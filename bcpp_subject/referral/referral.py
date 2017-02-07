from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from edc_constants.constants import (
    POS, NEG, MALE, FEMALE, DECLINED, NAIVE, NOT_APPLICABLE)
from edc_map.site_mappers import site_mappers

from ..models import (
    ReproductiveHealth, ResidencyMobility, is_circumcised, HivCareAdherence)
from ..subject_helper import SubjectHelper, ON_ART, DEFAULTER
from .choices import REFERRAL_CODES
from .referral_appt import ReferralAppt
from bcpp_subject.referral.constants import URGENT_REFERRALS
from edc_metadata.models import CrfMetadata
from edc_metadata.constants import REQUIRED, KEYED


class ReferralError(Exception):
    pass


class CdcReferral:

    def __init__(self, referral, **kwargs):
        self.on_art = None
        self.arv_clinic = None
        self.arv_documentation = referral.subject_helper.arv_evidence
        if referral.hiv_care_adherence:
            self.arv_clinic = referral.hiv_care_adherence.clinic_receiving_from
        self.citizen = referral.subject_referral.subject_visit.household_member.citizen
        self.citizen_spouse = (
            referral.subject_referral.subject_visit.household_member.spouse_of_citizen)
        self.direct_hiv_documentation = referral.subject_helper.documented_pos
        self.gender = referral.gender
        self.hiv_result_date = referral.subject_helper.final_hiv_status_date
        self.last_hiv_result = referral.subject_helper.prev_result
        self.last_hiv_result_date = referral.subject_helper.prev_result_date
        self.new_pos = referral.subject_helper.newly_diagnosed

        self.part_time_resident = (
            referral.subject_referral.subject_visit.household_member.study_resident)
        self.subject_identifier = referral.subject_identifier
        self.todays_hiv_result = referral.subject_helper.today_hiv_result
        self.verbal_hiv_result = referral.subject_helper.self_reported_result
#         self.cd4_result = self.subject_helper.cd4_result
#         self.cd4_result_datetime = self.subject_helper.cd4_result_datetime
#         self.vl_sample_drawn = self.subject_helper.vl_sample_drawn
#         self.vl_sample_drawn_datetime = self.subject_helper.vl_sample_drawn_datetime
#         self.indirect_hiv_documentation = self.subject_helper.indirect_hiv_documentation
        self.hiv_result = referral.subject_helper.final_hiv_status
        if referral.subject_helper.final_hiv_status == POS:
            self.on_art = True if referral.subject_helper.final_arv_status in [
                ON_ART, DEFAULTER] else False
        self.defaulter = (
            True if referral.subject_helper.final_arv_status == DEFAULTER else False)

        self.original_scheduled_appt_date = (
            referral.referral_appt.original_scheduled_appt_date)
        self.referral_appt_datetime = referral.referral_appt.referral_appt_datetime
        self.referral_clinic = referral.referral_appt.community_name
        self.referral_clinic_type = referral.referral_appt.referral_clinic_type
        self.circumcised = NOT_APPLICABLE if self.gender == FEMALE else referral.circumcised
        TbSymptoms = django_apps.get_model(
            *'bcpp_subject.tbsymptoms'.split('.'))
        self.tb_symptoms = TbSymptoms.objects.get_symptoms(
            referral.subject_referral.subject_visit)
        try:
            residency_mobility_instance = ResidencyMobility.objects.get(
                subject_visit=self.subject_visit)
        except ResidencyMobility.DoesNotExist:
            self.permanent_resident = None
        else:
            self.permanent_resident = residency_mobility_instance.permanent_resident


class Referral:
    """A class that calculates the referral code or returns
    a blank string.
    """

    def __init__(self, subject_visit=None, **kwargs):
        self.subject_helper = SubjectHelper(subject_visit)
        self.gender = subject_visit.household_member.gender
        self.subject_identifier = (
            subject_visit.appointment.subject_identifier)
        self.subject_visit = subject_visit

        # ReproductiveHealth, pregnant
        try:
            reproductive_health = ReproductiveHealth.objects.get(
                subject_visit=subject_visit)
        except ReproductiveHealth.DoesNotExist:
            self.pregnant = None
        else:
            self.pregnant = reproductive_health.currently_pregnant

        # HivCareAdherence
        try:
            self.hiv_care_adherence = HivCareAdherence.objects.get(
                subject_visit=subject_visit)
        except HivCareAdherence.DoesNotExist:
            self.hiv_care_adherence = None

        # SubjectReferral
        try:
            self.subject_referral = subject_visit.subjectreferral
        except ObjectDoesNotExist:
            self.subject_referral = None

        # CD4
        try:
            pima_cd4 = subject_visit.pimacd4
        except ObjectDoesNotExist:
            self.cd4_result = None
            self.cd4_result_datetime = None
        else:
            self.cd4_result = pima_cd4.cd4_value
            self.cd4_result_datetime = pima_cd4.cd4_datetime

        self.circumcised = None if self.gender == FEMALE else is_circumcised(
            subject_visit)

        # scheduled_appt_date
        try:
            scheduled_appt_date = self.hiv_care_adherence.next_appointment_date
        except AttributeError:
            try:
                scheduled_appt_date = self.subject_referral.scheduled_appt_date
            except AttributeError:
                scheduled_appt_date = None

        # from referral appt
        self.referral_appt = ReferralAppt(
            self.referral_code,
            base_date=subject_visit.report_datetime,
            scheduled_appt_date=scheduled_appt_date)

        # from mapper
        self.intervention = site_mappers.get_mapper(
            site_mappers.current_map_area).intervention
        self.community_code = site_mappers.get_mapper(
            site_mappers.current_map_area).map_code

        self.valid_referral_codes = [
            code for code, _ in REFERRAL_CODES if not code == 'pending']
        self.urgent_referral = self.referral_code in URGENT_REFERRALS

    def __str__(self):
        return '({0.subject_referral!r})'.format(self)

    @property
    def referral_code(self):
        """Returns a referral code or None.
         """
        referral_code = None
        try:
            is_declined = (
                True if self.subject_helper.hiv_result == DECLINED else False)
        except AttributeError:
            is_declined = None
        if not self.subject_helper.final_hiv_status or is_declined:
            referral_code = self.referral_code_for_untested
        else:
            referral_code = self.referral_code_for_tested
        return referral_code

    @property
    def referral_code_for_untested(self):
        """Returns a referral code or None.
        """
        referral_code = None
        if self.gender == MALE:
            if self.circumcised:
                referral_code = 'TST-HIV'
            else:
                if not self.circumcised:
                    referral_code = 'SMC-UNK'
                else:
                    referral_code = 'SMC?UNK'
        elif self.gender == FEMALE:
            if self.pregnant:
                referral_code = 'UNK?-PR'
            else:
                referral_code = 'TST-HIV'
        return referral_code

    @property
    def referral_code_for_tested(self):
        """Returns a referral code or None.
        """
        if self.subject_helper.indeterminate:
            referral_code = 'TST-IND'
        elif self.subject_helper.final_hiv_status == NEG:
            referral_code = self.referral_code_for_neg
        elif self.subject_helper.final_hiv_status == POS:
            referral_code = self.referral_code_for_pos
        else:
            referral_code = 'TST-HIV'
        return referral_code

    @property
    def referral_code_for_neg(self):
        """Returns a referral code or None.
        """
        referral_code = None
        if self.gender == FEMALE and self.pregnant:
            referral_code = 'NEG!-PR'
        elif self.gender == MALE and not self.circumcised:
            referral_code = 'SMC-NEG'
        return referral_code

    @property
    def referral_code_for_pos_naive(self):
        """Returns a referral code or None.
        """
        referral_code = None
        if not self.cd4_result:
            referral_code = 'TST-CD4'
        elif self.cd4_result and self.cd4_result > 500:
            referral_code = 'POS!-HI' if self.subject_helper.newly_diagnosed else 'POS#-HI'
        elif self.cd4_result and self.cd4_result <= 500:
            referral_code = 'POS!-LO' if self.subject_helper.newly_diagnosed else 'POS#-LO'
        return referral_code

    @property
    def referral_code_for_pos(self):
        referral_code = None
        if (self.gender == FEMALE
                and self.pregnant
                and self.subject_helper.final_arv_status == ON_ART):
            referral_code = 'POS#-AN'
        elif (self.gender == FEMALE
              and self.pregnant
              and self.subject_helper.final_arv_status == NAIVE):
            referral_code = (
                'POS!-PR' if self.subject_helper.newly_diagnosed else 'POS#-PR')
        elif self.subject_helper.final_arv_status == NAIVE:
            referral_code = self.referral_code_for_pos_naive
        elif self.subject_helper.final_arv_status == ON_ART:
            referral_code = 'MASA-CC'
        elif self.subject_helper.final_arv_status == DEFAULTER:
            referral_code = 'MASA-DF'
        return referral_code

    def previous_subject_referrals(self):
        internal_identifier = (
            self.subject_referral.subject_visit.household_member.internal_identifier)
        return (
            self.subject_referral.__class__.objects.filter(
                subject_visit__household_member__internal_identifier=internal_identifier,
                report_datetime__lt=self.subject_referral.report_datetime).order_by(
                    'report_datetime'))

    @property
    def cd4_required(self):
        try:
            return CrfMetadata.objects.get(
                model='bcpp_subject.pimacd4',
                entry_status__in=[REQUIRED, KEYED],
                visit_code=self.subject_visit.visit_code,
                subject_identifier=self.subject_visit.subject_identifier)
        except CrfMetadata.DoesNotExist:
            return None
