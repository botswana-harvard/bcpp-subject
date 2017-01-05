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
        self.subject_visit_female = self.make_subject_visit_for_consented_subject('T0')
        self.household_member = HouseholdMember.objects.filter(
            subject_identifier=self.subject_visit_male.subject_identifier)
        self.subject_identifier = self.subject_visit_male.subject_identifier

    def crf_metadata_obj(self, model, entry_status):
        return CrfMetadata.objects.filter(
            entry_status=entry_status,
            model=model,
            subject_identifier=self.subject_identifier)

    def test_hiv_car_adherence_and_pima1(self):
        """ HIV Positive took arv in the past but now defaulting, Should NOT offer POC CD4.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED).count(), 1)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=YES,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )
        # said they have taken ARV so not required
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, ).count(), 1)

    def test_hiv_car_adherence_and_pima2(self):
        """If POS and on arv and have doc evidence, Pima not required, not a defaulter.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_identifier = self.subject_visit_female.subject_identifier

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED).count(), 1)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_female,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=YES,
        )
        # on art so no need for CD4
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

    def test_hiv_car_adherence_and_pima3(self):
        """If POS and on arv but do not have doc evidence, Pima required.

        Models:
            * HivCareAdherence
            * HivResult
        """

        self.subject_identifier = self.subject_visit_male.subject_identifier

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED).count(), 1)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=NO,
        )
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)
