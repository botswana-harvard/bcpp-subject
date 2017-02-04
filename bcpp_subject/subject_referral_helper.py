from copy import copy
from collections import namedtuple

from django.apps import apps as django_apps

from edc_map.site_mappers import site_mappers
from edc_constants.constants import POS, NEG, MALE, IND, FEMALE, YES, NO
from edc_metadata.models import CrfMetadata
from edc_metadata.constants import REQUIRED
from survey.site_surveys import site_surveys

from .choices import REFERRAL_CODES
from .constants import ANNUAL_CODES, BASELINE_CODES, BASELINE, ANNUAL, DECLINED
from .models import (
    SubjectConsent, ResidencyMobility, Circumcision, ReproductiveHealth, SubjectLocator,
    HivCareAdherence)
from .subject_helper import SubjectHelper
from .subject_referral_appt_helper import SubjectReferralApptHelper
from .utils import convert_to_nullboolean
from bcpp_subject.subject_helper import ON_ART


class SubjectReferralHelper(object):
    """A class that calculates the referral code or returns
    a blank string.
    """

    def __init__(self, subject_referral):
        self._circumcised = None
        self._pregnant = None
        self._referral_clinic = None
        self._referral_code = None
        self._referral_code_list = []
        self._consent = None
        self._subject_referral_dict = {}

        self.subject_referral = subject_referral
        self.subject_helper = SubjectHelper(subject_referral.subject_visit)
        self.gender = subject_referral.subject_visit.household_member.gender
        self.subject_identifier = subject_referral.subject_visit.appointment.subject_identifier
        self.subject_visit = subject_referral.subject_visit
        self.visit_code = subject_referral.subject_visit.appointment.visit_code
        self.hiv_result = self.subject_helper.final_hiv_status
        self.on_art = None
        if self.subject_helper.final_hiv_status == ON_ART:
            self.on_art = self.subject_helper.final_hiv_status
        self.part_time_resident = self.subject_referral.household_member.study_resident
        self.tb_symptoms = subject_referral.tb_symptoms
        self.citizen = (self.consent.citizen == YES and self.consent.identity)
        self.citizen_spouse = (
            self.consent.citizen == NO and
            self.consent.legal_marriage == YES and
            self.consent.identity)

        try:
            self.arv_clinic = (
                self.subject_helper
                .hiv_care_adherence_instance
                .clinic_receiving_from)
        except AttributeError:
            self.arv_clinic = None

        self.intervention = site_mappers.get_mapper(
            site_mappers.current_map_area).intervention
        self.community_code = site_mappers.get_mapper(
            site_mappers.current_map_area).map_code
        # self.models dict is also used in the signal
        self.models = copy(self.subject_helper.models)
        self.models[BASELINE].update({
            'subject_locator': SubjectLocator,
            'circumcision': Circumcision,
            'reproductive_health': ReproductiveHealth,
            'residency_mobility': ResidencyMobility,
            'subject_consent': SubjectConsent,
        })
        self.models[ANNUAL].update({
            'subject_locator': SubjectLocator,
            'circumcision': Circumcision,
            'reproductive_health': ReproductiveHealth,
            'residency_mobility': ResidencyMobility,
            'subject_consent': SubjectConsent,
        })
        SubjectRequisition = django_apps.get_model(
            *'bcpp_subject.subjectrequisition'.split('.'))
        self.models[BASELINE].update(
            {'subject_requisition': SubjectRequisition})
        self.models[ANNUAL].update({'subject_requisition': SubjectRequisition})
        # prepare a queryset of visits previous to visit_instance
        SubjectReferral = django_apps.get_model(
            *'bcpp_subject.subjectreferral'.split('.'))
        internal_identifier = subject_referral.subject_visit.household_member.internal_identifier
        self.previous_subject_referrals = SubjectReferral.objects.filter(
            subject_visit__household_member__internal_identifier=internal_identifier,
            report_datetime__lt=subject_referral.report_datetime).order_by('report_datetime')
        self.valid_referral_codes = [
            code for code, _ in REFERRAL_CODES if not code == 'pending']

    def __str__(self):
        return '({0.subject_referral!r})'.format(self)

    @property
    def consent(self):
        # FIXME:
        if not self._consent:
            self._consent = (
                self.subject_referral.CONSENT_MODEL.consent.consent_for_period(
                    self.subject_identifier, self.subject_referral.report_datetime))
        return self._consent

    @property
    def required_crfs(self):
        """ Returns crf that are required to be keyed before subject
        referral.
        """
        crfs = ['bcpp_subject.subjectlocator',
                'bcpp_subject.hivresult',
                'bcpp_subject.elisahivresult',
                'bcpp_subject.hivresultdocumentation',
                'bcpp_subject.hivtestreview',
                'bcpp_subject.pimacd4',
                'bcpp_subject.hivtestinghistory']
        for crf in crfs:
            try:
                CrfMetadata.objects.get(
                    model=crf,
                    subject_identifier=self.subject_identifier,
                    entry_status=REQUIRED,
                    visit_code=self.visit_code)
                return django_apps.get_app_config(
                    crf.split('.')[0]).get_model(crf.split('.')[1])
            except CrfMetadata.DoesNotExist:
                pass

    @property
    def timepoint_key(self):
        """Returns a dictionary key of either baseline or annual base
         in the visit code.
         """
        if self.visit_code in BASELINE_CODES:
            return BASELINE
        return ANNUAL

    @property
    def subject_referral_dict(self):
        """Returns a dictionary of the attributes {name: value, ...}
        from this class that match, by name, field attributes in the
        SubjectReferral model.
        """
        if not self._subject_referral_dict:
            self._subject_referral_dict = {}
            for attr in self.subject_referral.__dict__:
                if attr in dir(self) and not attr.startswith('_'):
                    self._subject_referral_dict.update(
                        {attr: getattr(self, attr)})
        return self._subject_referral_dict

    @property
    def subject_referral_tuple(self):
        """Returns a dictionary of the attributes {name: value, ...}
        from this class that match, by name, field attributes in the
        SubjectReferral model.
        """
        Tpl = namedtuple(
            'SubjectReferralTuple', 'subject_visit ' +
            '  '.join(self.subject_referral.keys()))
        self._subject_referral_tuple = Tpl(
            self.subject_visit, *self.subject_referral.values())
        return self._subject_referral_tuple

    def male_referral_code(self):
        """ docstring is required"""
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
        """ Docstring is required"""
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
        """ Docstring is required"""
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

    @property
    def referral_code_list(self):
        """Returns a list of referral codes by reviewing the conditions
         for referral.
         """
        if not self._referral_code_list:
            is_declined = None
            try:
                is_declined = True if self.hiv_result == DECLINED else False
            except AttributeError:
                pass
            if not self.hiv_result or is_declined:
                if self.gender == MALE:
                    self.male_referral_code()
                elif self.pregnant:
                    self._referral_code_list.append('UNK?-PR')
                else:
                    self._referral_code_list.append('TST-HIV')
            else:
                self.referral_code_list_with_hiv_result()
            # refer if on art and known positive to get VL,
            # and o get outsiders to transfer care
            # referal date is the next appointment date if on art
            if self._referral_code_list:
                self._referral_code_list = list(
                    set((self._referral_code_list)))
                self._referral_code_list.sort()
                for code in self._referral_code_list:
                    if code not in self.valid_referral_codes:
                        raise ValueError(
                            '{0} is not a valid referral code.'.format(code))
        return self._referral_code_list

    @property
    def referral_code(self):
        """Returns a string of referral codes as a join of the
        list of referral codes delimited by ",".
        """
        if self._referral_code is None:
            self._referral_code = ','.join(self.referral_code_list)
            self._referral_code = self.remove_smc_in_annual_ecc(
                self._referral_code)
        return self._referral_code

    def remove_smc_in_annual_ecc(self, referral_code):
        """Removes any SMC referral codes if in the ECC during an ANNUAL survey."""
        survey_schedule = self.subject_visit.household_member.household_structure.survey_schedule
        code = referral_code.replace(
            'SMC-NEG', '').replace('SMC?NEG', '').replace('SMC-UNK', '').replace('SMC?UNK', '')
        if (not self.intervention
                and survey_schedule != site_surveys.current_surveys[0]):
            referral_code = code
        return referral_code

    @property
    def circumcised(self):
        """Returns None if female otherwise True if circumcised or False if not."""
        if self._circumcised is None:
            if self.gender == MALE:
                circumcised = None
                if self.previous_subject_referrals:
                    # save current visit
                    previous_subject_referrals = copy(
                        self.previous_subject_referrals)
                    for subject_referral in previous_subject_referrals:
                        # check for CIRCUMCISED result from previous data
                        circumcised = subject_referral.circumcised
                        if circumcised:
                            break
                if not circumcised:
                    try:
                        circumcision_instance = self.models[self.timepoint_key].get(
                            'circumcision').objects.get(subject_visit=self.subject_visit)
                        circumcised = convert_to_nullboolean(
                            circumcision_instance.circumcised)
                    except self.models[self.timepoint_key].get('circumcision').DoesNotExist:
                        circumcised = None
                self._circumcised = circumcised
        return self._circumcised

    @property
    def permanent_resident(self):
        """Returns True if permanent resident as stated on
        ResidencyMobility.
        """
        try:
            residency_mobility_instance = self.models[
                self.timepoint_key].get('residency_mobility').objects.get(
                subject_visit=self.subject_visit)
            permanent_resident = convert_to_nullboolean(
                residency_mobility_instance.permanent_resident)
        except self.models[self.timepoint_key].get('residency_mobility').DoesNotExist:
            permanent_resident = None
        return permanent_resident

    @property
    def pregnant(self):
        """Returns None if male otherwise True if pregnant or
        False if not.
        """
        if self.gender == FEMALE:
            if not self._pregnant:
                try:
                    reproductive_health = self.models[
                        self.timepoint_key].get('reproductive_health').objects.get(
                        subject_visit=self.subject_visit)
                    self._pregnant = convert_to_nullboolean(
                        reproductive_health.currently_pregnant)
                except self.models[self.timepoint_key].get(
                        'reproductive_health').DoesNotExist:
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

    @property
    def subject_referral_appt_helper(self):
        try:
            hiv_care_adherence = HivCareAdherence.objects.get(
                subject_visit=self.subject_visit)
        except HivCareAdherence.DoesNotExist:
            next_appointment = None
        else:
            next_appointment = hiv_care_adherence.next_appointment_date
        return SubjectReferralApptHelper(
            self.referral_code,
            base_date=self.subject_referral.report_datetime,
            scheduled_appt_date=self.subject_referral.scheduled_appt_date,
            hiv_care_adherence_next_appointment=next_appointment
        )

    @property
    def referral_appt_datetime(self):
        return self.subject_referral_appt_helper.referral_appt_datetime

    @property
    def referral_clinic_type(self):
        return self.subject_referral_appt_helper.referral_clinic_type

    @property
    def referral_clinic(self):
        return self.subject_referral_appt_helper.community_name

    @property
    def original_scheduled_appt_date(self):
        return self.subject_referral_appt_helper.original_scheduled_appt_date

    @property
    def new_pos(self):
        return self.subject_helper.new_pos

    @property
    def todays_hiv_result(self):
        return self.subject_helper.todays_hiv_result

    @property
    def hiv_result_datetime(self):
        return self.subject_helper.hiv_result_datetime

    @property
    def last_hiv_result_date(self):
        return self.subject_helper.last_hiv_result_date

    @property
    def verbal_hiv_result(self):
        return self.subject_helper.verbal_hiv_result

    @property
    def last_hiv_result(self):
        return self.subject_helper.last_hiv_result

    @property
    def indirect_hiv_documentation(self):
        return self.subject_helper.indirect_hiv_documentation

    @property
    def direct_hiv_documentation(self):
        return self.subject_helper.direct_hiv_documentation

    @property
    def defaulter(self):
        return self.subject_helper.defaulter

    @property
    def cd4_result(self):
        return self.subject_helper.cd4_result

    @property
    def vl_sample_drawn(self):
        return self.subject_helper.vl_sample_drawn

    @property
    def vl_sample_drawn_datetime(self):
        return self.subject_helper.vl_sample_drawn_datetime

    @property
    def arv_documentation(self):
        return self.subject_helper.arv_documentation

    @property
    def cd4_result_datetime(self):
        return self.subject_helper.cd4_result_datetime
