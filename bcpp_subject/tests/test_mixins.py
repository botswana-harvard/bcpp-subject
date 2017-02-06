from datetime import datetime
from dateutil.relativedelta import relativedelta

from faker import Faker
from model_mommy import mommy

from edc_base_test.exceptions import TestMixinError
from edc_base_test.mixins import (
    AddVisitMixin, CompleteCrfsMixin as BaseCompleteCrfsMixin)
from edc_base_test.mixins import LoadListDataMixin, DatesTestMixin
from edc_constants.constants import NO, YES, NOT_APPLICABLE, MALE
from edc_metadata.models import CrfMetadata

from household.tests.household_test_mixin import HouseholdTestMixin
from household.constants import ELIGIBLE_REPRESENTATIVE_PRESENT
from member.constants import HEAD_OF_HOUSEHOLD
from member.list_data import list_data
from member.models.enrollment_checklist import EnrollmentChecklist
from member.models import HouseholdMember
from member.tests.mixins import MemberTestMixin
from plot.tests.plot_test_mixin import PlotTestMixin
from survey.tests import (
    SurveyTestMixin, DatesTestMixin as SurveyDatesTestMixin)

from ..constants import T0, E0
from ..models import Appointment
from edc_consent.site_consents import site_consents
from django.db.utils import IntegrityError
from bcpp_subject.models.subject_consent import SubjectConsent
from django.db import transaction
from edc_registration.models import RegisteredSubject
from bcpp_subject.constants import T2

fake = Faker()


class SubjectTestMixin:

    def setUp(self):
        super().setUp()

        self.consent_data_male = {
            'identity': '317115158', 'confirm_identity': '317115158', }

        survey_schedule = self.get_survey_schedule(index=2)
        self.subject_visit_male = self.make_subject_visit_for_consented_subject_male(
            E0,
            survey_schedule=survey_schedule,
            **self.consent_data_male)

        self.consent_data_male_t0 = {
            'identity': '317115159', 'confirm_identity': '317115159', }
        self.subject_visit_male_t0 = self.make_subject_visit_for_consented_subject_male(
            T0,
            survey_schedule=self.get_survey_schedule(index=1),
            **self.consent_data_male_t0)

        self.consent_data_female = {
            'identity': '317221515',
            'confirm_identity': '317221515', }
        survey_schedule = self.get_survey_schedule(index=2)
        self.subject_visit_female = self.make_subject_visit_for_consented_subject_female(
            E0,
            survey_schedule=survey_schedule,
            **self.consent_data_female)

        self.study_site = '40'

    def add_subject_consent(self, household_member=None,
                            survey_schedule=None, **options):
        """Returns a subject consent.

            * Consents the given `household_member`.
              If `household_member`=None will create one using
                `options` then consent him/her.
            * Adds the enrollment checklist for the `household_member`,
              if it does not exist.
            * Creates a HoH household member if one does not already
              exist.
        """

        if household_member and survey_schedule:
            raise TestMixinError(
                'If \'household_member\' is specified, \'survey_'
                'schedule\' is not required.')

        if not household_member:
            survey_schedule = survey_schedule or self.get_survey_schedule(0)
            household_structure = self.make_household_ready_for_enumeration(
                make_hoh=False, survey_schedule=survey_schedule)
            household_member = self.add_household_member(
                household_structure,
                relation=HEAD_OF_HOUSEHOLD,
                **options)
            self.assertTrue(household_member.eligible_member)
        else:
            household_structure = household_member.household_structure

        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(
                household_member=household_member)
            self.assertTrue(enrollment_checklist.is_eligible)
        except EnrollmentChecklist.DoesNotExist:
            self.assertTrue(
                household_member.eligible_member)
            household_member = self.add_enrollment_checklist(
                household_member, **options)
            household_member = HouseholdMember.objects.get(
                pk=household_member.pk)
            self.assertTrue(household_member.eligible_subject)
            enrollment_checklist = household_member.enrollmentchecklist
        # update options for subject consent from enrollment checklist
        report_datetime = options.get(
            'report_datetime') or self.get_utcnow()
        consent_object = site_consents.get_consent(
            report_datetime=report_datetime,
            consent_model='bcpp_subject.subjectconsent')

        # fake values
        fake_identity = fake.credit_card_number()
        last_name = fake.last_name().upper()
        initials = options.get(
            'initials', enrollment_checklist.initials)
        last_name = initials[1] + last_name

        # if RegisteredSubject exists, use those values unless
        # explicitly provided through 'options'
        # see UpdatesOrCreatesRegistrationModelMixin in subject_consent
        try:
            registered_subject = RegisteredSubject.objects.get(
                registration_identifier=household_member.internal_identifier)
        except RegisteredSubject.DoesNotExist:
            identity = options.get('identity', fake_identity)
            confirm_identity = options.get('confirm_identity', fake_identity)
            dob = options.get('dob', enrollment_checklist.dob)
        else:
            identity = options.get('identity', registered_subject.identity)
            confirm_identity = options.get(
                'confirm_identity', registered_subject.identity)
            dob = options.get('dob', registered_subject.dob)
        consent_options = dict(
            first_name=household_member.first_name,
            last_name=last_name,
            version=consent_object.version,
            consent_datetime=report_datetime,
            dob=dob,
            gender=options.get('gender', enrollment_checklist.gender),
            initials=initials,
            is_literate=options.get(
                'is_literate', enrollment_checklist.literacy),
            witness_name=options.get(
                'witness_name',
                fake.last_name() if enrollment_checklist.literacy == NO else None),
            legal_marriage=options.get(
                'legal_marriage', enrollment_checklist.legal_marriage),
            marriage_certificate=options.get(
                'marriage_certificate',
                enrollment_checklist.marriage_certificate),
            guardian_name=options.get(
                'guardian_name',
                fake.name() if enrollment_checklist.guardian == YES else None),
            identity=identity,
            confirm_identity=confirm_identity)

        # add subject consent
        with transaction.atomic():
            try:
                subject_consent = mommy.make_recipe(
                    'bcpp_subject.subjectconsent',
                    household_member=household_member,
                    survey_schedule=household_member.survey_schedule_object.field_value,
                    **consent_options)
            except IntegrityError:
                subject_consent = None
        if not subject_consent:
            # subject consent not added, fetching existing
            subject_consent = SubjectConsent.objects.get(
                subject_identifier=household_member.subject_identifier,
                version=consent_object.version)
        return subject_consent

    def add_subject_visits(self, visit_codes, subject_identifier):
        return self.add_visits(
            *visit_codes,
            model_label=self.bcpp_subject_model_label,
            subject_identifier=subject_identifier)

    def make_subject_visit_for_consented_subject_female(
            self, visit_code, report_datetime=None, survey_schedule=None, **options):
        """Returns a subject visit the given visit_code.

        Creates all needed relations."""
        household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=survey_schedule)
        household_member = self.add_household_member(
            household_structure=household_structure)
        household_member = self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member, **options)
        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=visit_code)
        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            subject_identifier=household_member.subject_identifier,
            appointment=appointment,
            report_datetime=report_datetime or self.get_utcnow())

    def make_subject_visit_for_consented_subject_male(
            self, visit_code, report_datetime=None, survey_schedule=None,
            **options):
        """Returns a subject visit of a consented male member.

        By default this is for the first survey_schedule.
        """
        household_structure = self.make_enumerated_household_with_male_member(
            survey_schedule=survey_schedule)
        household_member = self.add_household_member(
            household_structure=household_structure, gender=MALE)
        household_member = self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member, **options)
        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=visit_code)
        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            subject_identifier=household_member.subject_identifier,
            appointment=appointment,
            report_datetime=report_datetime or self.get_utcnow())

    def add_subject_visit_followup(self, previous_member, visit_code,
                                   household_log_report_date=None, create_consent=None, **options):

        next_household_structure = self.get_next_household_structure_ready(
            previous_member.household_structure, make_hoh=None)
        report_datetime = options.get(
            'report_datetime') or next_household_structure.enumerated_datetime
        new_household_member = previous_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)
        new_household_member.save()

        new_household_member.inability_to_participate = NOT_APPLICABLE
        new_household_member.study_resident = YES
        new_household_member.save()

        new_household_member = HouseholdMember.objects.get(
            pk=new_household_member.pk)
        report_datetime = report_datetime or self.get_utcnow(
        ) + relativedelta(years=1, months=6)
        household_log_report_date = household_log_report_date or datetime(
            2010, 3, 5)
        mommy.make_recipe(
            'household.householdlogentry',
            report_datetime=household_log_report_date,
            household_log=new_household_member.household_structure.householdlog,
            household_status=ELIGIBLE_REPRESENTATIVE_PRESENT)
        if not visit_code == T2:
            self.consent_data.update(report_datetime=report_datetime)
            self.add_subject_consent(
                new_household_member, **self.consent_data)
        else:
            consent = SubjectConsent.objects.filter(
                subject_identifier=new_household_member.subject_identifier).last()
            report_datetime = consent.report_datetime
        appointment = Appointment.objects.get(
            subject_identifier=new_household_member.subject_identifier,
            visit_code=visit_code)

        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=new_household_member,
            subject_identifier=new_household_member.subject_identifier,
            appointment=appointment,
            report_datetime=report_datetime)


class CompleteCrfsMixin(BaseCompleteCrfsMixin):

    def complete_required_subject_crfs(self, visit_codes, subject_identifier):
        """Complete all required CRFs for a visit(s) using mommy defaults."""
        complete_required_crfs = {}
        for visit_code in visit_codes:
            subject_visit = self.add_subject_visits(
                visit_code, subject_identifier)
            completed_crfs = super().complete_required_crfs(
                visit_code=visit_code,
                visit=subject_visit,
                visit_attr='subject_visit',
                subject_identifier=subject_identifier)
            complete_required_crfs.update({visit_code: completed_crfs})
        return complete_required_crfs

    def get_crfs(self, visit_code=None, subject_identifier=None):
        """Return a queryset of crf metadata for the visit."""
        return CrfMetadata.objects.filter(
            subject_identifier=subject_identifier,
            visit_code=visit_code).exclude(
                model__in=['bcpp_subject.hivresult',
                           'bcpp_subject.subjectreferral']).order_by(
                               'show_order')


class SubjectMixin(PlotTestMixin, HouseholdTestMixin, SurveyTestMixin,
                   MemberTestMixin, CompleteCrfsMixin, AddVisitMixin,
                   SubjectTestMixin, SurveyDatesTestMixin,
                   DatesTestMixin, LoadListDataMixin):

    bcpp_subject_model_label = 'bcpp_subject.subjectvisit'
    list_data = list_data
