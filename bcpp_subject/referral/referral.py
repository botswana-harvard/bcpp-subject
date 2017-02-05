from django.apps import apps as django_apps

from edc_constants.constants import POS, NEG, MALE, IND, FEMALE, DECLINED
from edc_map.site_mappers import site_mappers

from survey.site_surveys import site_surveys

from ..models import (
    ReproductiveHealth, ResidencyMobility, is_circumcised)
from ..subject_helper import SubjectHelper, ON_ART, DEFAULTER
from ..utils import convert_to_nullboolean
from .choices import REFERRAL_CODES
from .constants import ANNUAL_CODES
from .referral_appt import ReferralAppt


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
        self.circumcised = is_circumcised(
            referral.subject_referral.subject_visit)
        TbSymptoms = django_apps.get_model(
            *'bcpp_subject.tbsymptoms'.split('.'))
        self.tb_symptoms = TbSymptoms.objects.get_symptoms(
            referral.subject_referral.subject_visit)


class Referral:
    """A class that calculates the referral code or returns
    a blank string.
    """

    def __init__(self, subject_referral=None, **kwargs):
        self._circumcised = None
        self._pregnant = None
        self._referral_clinic = None
        self._referral_code_list = []
        self._consent = None
        self._subject_referral_dict = {}
        self.subject_referral = subject_referral
        self.subject_helper = SubjectHelper(subject_referral.subject_visit)
        self.gender = subject_referral.subject_visit.household_member.gender
        self.subject_identifier = (
            subject_referral.subject_visit.appointment.subject_identifier)
        self.subject_visit = subject_referral.subject_visit

        if self.hiv_care_adherence:
            scheduled_appt_date = (
                subject_referral.scheduled_appt_date
                or self.hiv_care_adherence.next_appointment_date)
        else:
            scheduled_appt_date = subject_referral.scheduled_appt_date

        # from referral appt
        self.referral_appt = ReferralAppt(
            subject_referral.referral_code,
            base_date=subject_referral.report_datetime,
            scheduled_appt_date=scheduled_appt_date)

        # from mapper
        self.intervention = site_mappers.get_mapper(
            site_mappers.current_map_area).intervention
        self.community_code = site_mappers.get_mapper(
            site_mappers.current_map_area).map_code

        self.valid_referral_codes = [
            code for code, _ in REFERRAL_CODES if not code == 'pending']

    def __str__(self):
        return '({0.subject_referral!r})'.format(self)

    @property
    def referral_code(self):
        """Returns a string of referral codes as a join of the
        list of referral codes delimited by ",".
        """
        referral_code = ','.join(self.referral_code_list)
        referral_code = self.remove_smc_in_annual_ecc(referral_code)
        return referral_code

    @property
    def referral_code_list(self):
        """Returns a list of referral codes by reviewing the conditions
         for referral.
         """
        is_declined = None
        referral_code = []
        try:
            is_declined = True if self.subject_helper.hiv_result == DECLINED else False
        except AttributeError:
            pass
        if not self.final_hiv_result or is_declined:
            if self.gender == MALE:
                self.male_referral_code()
            elif self.pregnant:
                referral_code_list.append('UNK?-PR')
            else:
                referral_code_list.append('TST-HIV')
        else:
            self.referral_code_list_with_hiv_result()
        # refer if on art and known positive to get VL,
        # and o get outsiders to transfer care
        # referal date is the next appointment date if on art
        if referral_code_list:
            referral_code_list = list(
                set((referral_code_list)))
            referral_code_list.sort()
            for code in referral_code_list:
                if code not in self.valid_referral_codes:
                    raise ValueError(
                        '{0} is not a valid referral code.'.format(code))
        return referral_code_list

    def male_referral_code(self):
        if self.circumcised:
            # refer if status unknown
            self._referral_code_list.append('TST-HIV')
        else:
            if self.circumcised is False:
                # refer if status unknown
                self._referral_code_list.append('SMC-UNK')
            else:
                # refer if status unknown
                self._referral_code_list.append('SMC?UNK')

    def referral_code_neg(self):
        if self.gender == FEMALE and self.pregnant:  # only refer F if pregnant
            self._referral_code_list.append('NEG!-PR')
        # only refer M if not circumcised
        elif self.gender == MALE and self.circumcised is False:
            self._referral_code_list.append('SMC-NEG')
        # only refer M if not circumcised
        elif self.gender == MALE and self.circumcised is None:
            self._referral_code_list.append('SMC?NEG')

    def referral_code_pos_not_on_art(self):
        if not self.cd4_result:
            self._referral_code_list.append('TST-CD4')
        elif self.cd4_result > (500 if self.intervention else 350):
            self._referral_code_list.append(
                'POS!-HI') if self.new_pos else self._referral_code_list.append('POS#-HI')
        elif self.cd4_result <= (500 if self.intervention else 350):
            self._referral_code_list.append(
                'POS!-LO') if self.new_pos else self._referral_code_list.append('POS#-LO')

    def referral_code_pos_on_art(self):
        self._referral_code_list.append('MASA-CC')
        if self.defaulter:
            self._referral_code_list = [
                'MASA-DF' for item in self._referral_code_list if item == 'MASA-CC']
        if self.pregnant:
            self._referral_code_list = [
                'POS#-AN' for item in self._referral_code_list if item == 'MASA-CC']
        # do not refer to MASA-CC except if BASELINE
        if self.visit_code in ANNUAL_CODES:
            try:
                self._referral_code_list.remove('MASA-CC')
            except ValueError:
                pass

    def referral_code_pos(self):
        if self.gender == FEMALE and self.pregnant and self.on_art:
            self._referral_code_list.append('POS#-AN')
        elif self.gender == FEMALE and self.pregnant and not self.on_art:
            self._referral_code_list.append(
                'POS!-PR') if self.new_pos else self._referral_code_list.append('POS#-PR')
        elif not self.on_art:
            self.referral_code_pos_not_on_art()
        elif self.on_art:
            self.referral_code_pos_on_art()

    def referral_code_list_with_hiv_result(self):
        if self.hiv_result == IND:
            # do not set referral_code_list to IND
            pass
        elif self.hiv_result == NEG:
            self.referral_code_neg()
        elif self.hiv_result == POS:
            self.referral_code_pos()
        else:
            self._referral_code_list.append('TST-HIV')

    def remove_smc_in_annual_ecc(self, referral_code):
        """Removes any SMC referral codes if in the ECC during
        an ANNUAL survey."""
        survey_schedule = (
            self.subject_visit.household_member.household_structure.survey_schedule)
        code = referral_code.replace(
            'SMC-NEG', '').replace('SMC?NEG', '').replace('SMC-UNK', '').replace('SMC?UNK', '')
        if (not self.intervention
                and survey_schedule != site_surveys.current_surveys[0]):
            referral_code = code
        return referral_code

    @property
    def permanent_resident(self):
        """Returns True if permanent resident as stated on
        ResidencyMobility.
        """
        try:
            residency_mobility_instance = ResidencyMobility.objects.get(
                subject_visit=self.subject_visit)
        except ResidencyMobility.DoesNotExist as e:
            raise ReferralError(e)
        return residency_mobility_instance.permanent_resident

    @property
    def pregnant(self):
        """Returns None if male otherwise True if pregnant or
        False if not.
        """
        if self.gender == FEMALE:
            if not self._pregnant:
                try:
                    reproductive_health = ReproductiveHealth.objects.get(
                        subject_visit=self.subject_visit)
                    self._pregnant = convert_to_nullboolean(
                        reproductive_health.currently_pregnant)
                except ReproductiveHealth.DoesNotExist:
                    self._pregnant = None
        return self._pregnant

    @property
    def urgent_referral(self):
        """Compares the referral_codes to the "urgent" referrals
        list and sets to true on a match.
        """
        URGENT_REFERRALS = [
            'MASA-DF', 'POS!-LO', 'POS#-LO',
            'POS!-HI', 'POS#-HI',
            'POS#-PR', 'POS!-PR']
        return True if[
            code for code in self.referral_code_list if code in URGENT_REFERRALS
        ] else False

    def previous_subject_referrals(self):
        internal_identifier = (
            self.subject_referral.subject_visit.household_member.internal_identifier)
        return (
            self.subject_referral.__class__.objects.filter(
                subject_visit__household_member__internal_identifier=internal_identifier,
                report_datetime__lt=self.subject_referral.report_datetime).order_by(
                    'report_datetime'))

    @property
    def hiv_care_adherence(self):
        HivCareAdherence = django_apps.get_model(
            *'bcpp_subject.hivcareadherence'.split('.'))
        try:
            return HivCareAdherence.objects.get(
                subject_visit=self.subject_referral.subject_visit)
        except HivCareAdherence.DoesNotExist:
            return None
