from django.test import TestCase

from edc_constants.constants import YES, NO

from .test_mixins import SubjectMixin

from bcpp_subject.forms.outpatient_care_form import OutpatientCareForm


class TestOutpatientCareForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.consent_data = {
            'identity': '31721515',
            'confirm_identity': '31721515',
            'report_datetime': self.get_utcnow(),
        }
        self.bhs_subject_visit_male = self.make_subject_visit_for_consented_subject_male('E0', **self.consent_data)
        self.options = {
            'subject_visit': self.bhs_subject_visit_male.id,
            'report_datetime': self.get_utcnow(),
            'govt_health_care': YES,
            'dept_care': YES,
            'prvt_care': NO,
            'trad_care': NO,
            'care_visits': 4,
            'facility_visited': 'Government Clinic/Post',
            'specific_clinic': None,
            'care_reason': 'Chronic disease',
            'care_reason_other': None,
            'outpatient_expense': 150.00,
            'travel_time': '0.5 to under 1 hour',
            'transport_expense': 50.00,
            'cost_cover': YES,
            'waiting_hours': 'Under 0.5 hour'
        }

    def test_form_is_valid(self):
        form = OutpatientCareForm(data=self.options)
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_if_participant_seeked_care_from_gov(self):
        """Assert to see if the participant visited govt clinic"""
        self.options.update(govt_health_care=YES, care_visits=None)
        form = OutpatientCareForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_participant_visited_govt_clinic_in_past_3_months(self):
        """Asserts if participant visted govt facility in the past 3 months"""
        self.options.update(govt_health_care=YES, care_visits=0)
        form = OutpatientCareForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_participant_visited_govt_clinic_with_valid_care_reason(self):
        """Assert if the primary reason for seeking care is the right care reason"""
        self.options.update(govt_health_care=YES, care_reason=None)
        form = OutpatientCareForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_participant_seeked_govt_care_and_have_ans_abt_facility(self):
        """Assert that care reason cannot be none"""
        self.options.update(govt_health_care=YES, facility_visited=None)
        form = OutpatientCareForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_participant_seeked_govt_care_then_paid_outpatient_expenses(self):
        """Assert that care provided then outpatient expenses were paid"""
        self.options.update(govt_health_care=YES, outpatient_expense=None)
        form = OutpatientCareForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_time_participant_take_to_health_care_facility(self):
        """Assert that time taken to the hospital was not none"""
        self.options.update(govt_health_care=YES, travel_time=None)
        form = OutpatientCareForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_time_participant_took_waiting_at_a_health_facility(self):
        """Assert that waiting hours was not none"""
        self.options.update(govt_health_care=YES, waiting_hours=None)
        form = OutpatientCareForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_care_reason_is_pregnancy_then_make_cannot_be_asked(self):
        """Assert that care reason being pregnancy then male shouldnt be consented"""
        self.options.update(govt_health_care=YES, care_reason='Pregnancy')
        form = OutpatientCareForm(data=self.options)
        self.assertFalse(form.is_valid())
