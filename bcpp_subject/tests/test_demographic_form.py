from django.test import TestCase
from model_mommy import mommy

from ..forms import DemographicsForm
from .test_mixins import SubjectMixin


class TestSubjectConsentForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        subject_visit = self.make_subject_visit_for_consented_subject('T0')

        self.religion = mommy.make_recipe('bcpp_subject.religion')
        self.ethics = mommy.make_recipe('bcpp_subject.ethics')
        self.livewith = mommy.make_recipe('bcpp_subject.livewith')

        self.data = {
            'ethnic_other': '',
            'husband_wives': 0,
            'marital_status': 'Married',
            'report_datetime': self.get_utcnow(),
            'num_wives': 2,
            'live_with': [self.livewith.id],
            'religion': [self.religion.id],
            'religion_other': u'',
            'subject_visit': subject_visit.id,
            'ethnic': [self.ethics.id]
        }

    def test_demographics_form_valid(self):
        demo_form = DemographicsForm(data=self.data)
        self.assertTrue(demo_form.is_valid())

    def test_marriage_gender_female_valid(self):
        """ Assert that is a participant is married and with number of wife less than zero validation error thrown"""
        self.data.update(num_wives=0, husband_wives=10)
        demo_form = DemographicsForm(data=self.data)
        self.assertFalse(demo_form.is_valid())

    def test_live_with_alone_valid(self):
        """ Assert that the many to many Alone can not be selected with another value."""
        livewith2 = mommy.make_recipe('bcpp_subject.livewith', name='Alone', short_name='Alone')
        self.data.update(live_with=[self.livewith.id, livewith2.id])
        form = DemographicsForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_live_with_don_not_want_to_answer_valid(self):
        """ Assert that the many to many Don\'t want to answer can not be selected with another value."""
        livewith2 = mommy.make_recipe('bcpp_subject.livewith', name='Don\'t want to answer', short_name='Don\'t want to answer')
        self.data.update(live_with=[self.livewith.id, livewith2.id])
        form = DemographicsForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_1_ethic_group_at_a_time(self):
        """ Assert that a participant can only be in 1 ethenic group."""
        ethnic2 = mommy.make_recipe('bcpp_subject.ethics', name='Bakgatla', short_name='Bakgatla')
        self.data.update(ethnic=[self.ethics.id, ethnic2.id])
        form = DemographicsForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_1_religion_group_at_a_time(self):
        """ Assert that a participant can only be in 1 religion."""
        religion2 = mommy.make_recipe('bcpp_subject.ethics', name='ZCC', short_name='ZCC')
        self.data.update(religion=[self.religion.id, religion2.id])
        form = DemographicsForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_unmarried_has_no_wives(self):
        """Assert that a unmarried participant can not have wives."""
        self.data.update(marital_status='Single/never married', num_wives=3)
        form = DemographicsForm(data=self.data)
        self.assertFalse(form .is_valid())

# TODO: Add more tests

#     def test_marriage_gender_female_not_valid(self):
#         """ Test identity on
#         """
#         self.data['num_wives'] = 10
#         self.data['husband_wives'] = None
#         from bhp066.apps.bcpp_subject.forms import DemographicsForm
#         demo_form = DemographicsForm(data=self.data)
#         self.assertFalse(demo_form.is_valid())
#         self.assertIn(
#             u"You should fill the number of wives.", demo_form.errors.get("__all__"))
#

# 
#     @override_settings(
#         SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
#         CURRENT_COMMUNITY_CHECK=False,
#         LIMIT_EDIT_TO_CURRENT_SURVEY=True,
#         LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
#         FILTERED_DEFAULT_SEARCH=True,
#     )
#     def test_marriage_gender_female_annual_notvalid(self):
#         """ Test identity on
#         """
#         enumeration_helper_T2 = EnumerationHelper(self.household_structure_bhs.household, self.survey_bhs, self.survey_ahs)
#         enumeration_helper_T2.add_members_from_survey()
#         self.data['num_wives'] = 10
#         self.data['husband_wives'] = None
#         self.household_member_male = HouseholdMember.objects.get(household_structure=self.household_structure_ahs)
#         self.subject_consent_male.version = 2
#         self.subject_consent_male.save_base()
#         self.subject_consent_male = SubjectConsentFactory(
#             household_member=self.household_member_male, confirm_identity='101119811', identity='101119811',
#             study_site=self.study_site, gender='M', dob=self.male_dob, first_name=self.male_first_name,
#             initials=self.male_initials, version=4)
# 
#         appointment_male = Appointment.objects.get(
#             registered_subject=self.household_member_male_T0.registered_subject, visit_definition__code='T1')
# 
#         subject_visit_male = SubjectVisitFactory(
#             appointment=appointment_male, household_member=self.household_member_male)
#         self.data['subject_visit'] = subject_visit_male.id
#         from bhp066.apps.bcpp_subject.forms import DemographicsForm
#         demo_form = DemographicsForm(data=self.data)
#         self.assertFalse(demo_form.is_valid())
#         self.assertIn(
#             u"You should fill the number of wives.", demo_form.errors.get("__all__"))
