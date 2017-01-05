from model_mommy import mommy

from django.test import TestCase

from edc_constants.constants import NO, YES
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata

from member.models.household_member import HouseholdMember

from .test_mixins import SubjectMixin


class TestBaselineRuleSurveyRuleGroups(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit_male = self.make_subject_visit_for_a_male_subject('T0')
        self.household_member = HouseholdMember.objects.filter(
            subject_identifier=self.subject_visit_male.subject_identifier)

    def test_hiv_car_adherence_and_pima1(self):
        """ HIV Positive took arv in the past but now defaulting, Should NOT offer POC CD4.

        Models:
            * HivCareAdherence
            * HivResult
        """
        crf_metada_hivcareadherence = CrfMetadata.objects.filter(
            entry_status=REQUIRED,
            model='bcpp_subject.hivcareadherence',
            subject_identifier=self.subject_visit_male.subject_identifier)
        self.assertEqual(crf_metada_hivcareadherence.count(), 1)

        crf_metada_pima = CrfMetadata.objects.filter(
            entry_status=NOT_REQUIRED,
            model='bcpp_subject.pima',
            subject_identifier=self.subject_visit_male.subject_identifier
        )
        self.assertEqual(crf_metada_pima.count(), 1)

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            subject_visit=self.subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=YES,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )
        # said they have taken ARV so not required
        self.assertEqual(crf_metada_pima.count(), 1)
