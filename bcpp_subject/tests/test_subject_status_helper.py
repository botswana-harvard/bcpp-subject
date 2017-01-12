import datetime

from model_mommy import mommy
from datetime import timedelta
from django.test import TestCase

from survey.site_surveys import site_surveys

from edc_constants.constants import NO, YES, POS, NEG
from edc_metadata.constants import REQUIRED, NOT_REQUIRED

from bcpp_subject.constants import T1, MICROTUBE, T0, RESEARCH_BLOOD_DRAW, VIRAL_LOAD
from bcpp_subject.subject_status_helper import SubjectStatusHelper

from ..models import Appointment

from .rule_group_mixins import RuleGroupMixin


class TestSubjectStatusHelper(RuleGroupMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit_male = self.make_subject_visit_for_a_male_subject('T0')
        self.hiv_test_date = self.get_utcnow() - timedelta(days=50)

    def ahs_y2_subject_visit(self):
        """Return an ahs subject visit."""
        # Create an ahs member
        survey = site_surveys.current_surveys[1]
        household_member = super().make_ahs_household_member(self.subject_visit_male.household_member, survey)
        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=T1)
        report_datetime = self.get_utcnow() + datetime.timedelta(3 * 365 / 12)
        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            subject_identifier=household_member.subject_identifier,
            appointment=appointment,
            report_datetime=report_datetime)

    def tests_hiv_result(self):
        """"""
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertIsNone(subject_status_helper.hiv_result)
        self.assertIsNone(subject_status_helper.new_pos)

        subject_status_helper = SubjectStatusHelper(self.ahs_y2_subject_visit())
        self.assertIsNone(subject_status_helper.hiv_result)
        self.assertIsNone(subject_status_helper.new_pos)

    def tests_hiv_result1(self):
        """"""
        report_datetime = self.get_utcnow() + datetime.timedelta(3 * 365 / 12)
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, NO)
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, YES, NO)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)

        self.assertIsNone(subject_status_helper.hiv_result)
        self.assertIsNone(subject_status_helper.new_pos)

        self.make_hivtesting_history(self.ahs_y2_subject_visit(), report_datetime, YES, NO, POS, NO)
        self.make_hiv_care_adherence(self.ahs_y2_subject_visit(), report_datetime, NO, YES, NO, YES, NO)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male_annual)
        self.assertIsNone(subject_status_helper.hiv_result)
        self.assertIsNone(subject_status_helper.new_pos)

    def tests_hiv_result2(self):
        """"""
        report_datetime = self.get_utcnow() + datetime.timedelta(3 * 365 / 12)
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, NO)
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, YES, NO)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertIsNone(subject_status_helper.hiv_result)
        self.assertIsNone(subject_status_helper.new_pos)

        ahs_y2_subject_visit = self.ahs_y2_subject_visit()
        self.make_hivtesting_history(ahs_y2_subject_visit, report_datetime, YES, NO, POS, NO)
        self.make_hiv_care_adherence(ahs_y2_subject_visit, report_datetime, NO, YES, NO, YES, NO)
        subject_status_helper = SubjectStatusHelper(ahs_y2_subject_visit)
        self.assertIsNone(subject_status_helper.hiv_result)
        self.assertIsNone(subject_status_helper.new_pos)

    def tests_hiv_result2a(self):
        """"""
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, YES, POS, NO)
        self.make_hivtest_review(self.subject_visit_male, POS, self.get_utcnow(), self.hiv_test_date)
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, YES, NO)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.hiv_result, POS)
        self.assertFalse(subject_status_helper.new_pos)

        ahs_y2_subject_visit = self.ahs_y2_subject_visit()
        self.make_hiv_care_adherence(ahs_y2_subject_visit, self.get_utcnow(), NO, YES, NO, YES, NO)
        self.make_hiv_care_adherence(ahs_y2_subject_visit, self.get_utcnow(), NO, YES, NO, YES, NO)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male_annual)
        self.assertEquals(subject_status_helper.hiv_result, POS)
        self.assertFalse(subject_status_helper.new_pos)

    def tests_hiv_result3(self):
        """"""

        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, YES)
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, YES, NO)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.hiv_result, POS)

        ahs_y2_subject_visit = self.ahs_y2_subject_visit()
        self.make_hiv_care_adherence(ahs_y2_subject_visit, self.get_utcnow(), NO, YES, NO, YES, NO)
        subject_status_helper = SubjectStatusHelper(ahs_y2_subject_visit)
        self.assertEquals(subject_status_helper.hiv_result, POS)

    def tests_hiv_result4a(self):
        """"""
        self.make_requisition(self.subject_visit_male, MICROTUBE, self.get_utcnow())
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, NO)
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, YES, NO)

        self.make_hiv_result(POS, self.subject_visit_male, self.get_utcnow())
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.hiv_result, POS)

        self.make_hiv_care_adherence(self.ahs_y2_subject_visit(), self.get_utcnow(), NO, YES, NO, YES, NO)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male_annual)
        self.assertEquals(subject_status_helper.hiv_result, POS)

    def tests_hiv_result4a1(self):
        """Asserts that hiv_result, result_datetime are carried over from baseline if
        HIV result is POS and at annual, new_pos is False."""

        report_datetime_baseline = self.subject_visit_male.report_datetime
        self.make_requisition(self.subject_visit_male, MICROTUBE, self.get_utcnow())
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, None, NO)
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, NO, NO)
        self.make_hiv_result(POS, self.subject_visit_male, self.get_utcnow())
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.hiv_result, POS)
        self.assertEquals(subject_status_helper.hiv_result_datetime.date(), report_datetime_baseline.date())
        self.assertEquals(subject_status_helper.new_pos, True)

        self.make_hiv_care_adherence(self.ahs_y2_subject_visit(), self.get_utcnow(), NO, YES, NO, YES, NO)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male_annual)
        self.assertEquals(subject_status_helper.hiv_result, POS)
        self.assertEquals(subject_status_helper.hiv_result_datetime.date(), report_datetime_baseline.date())
        self.assertEquals(subject_status_helper.new_pos, False)

    def tests_hiv_result4a2(self):
        """"""
        self.make_requisition(self.subject_visit_male, MICROTUBE, self.get_utcnow())

        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, None, NO)
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, NO, NO)
        self.make_hiv_result(NEG, self.subject_visit_male, self.get_utcnow())
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)

        self.assertEquals(subject_status_helper.hiv_result, NEG)
        self.assertEquals(subject_status_helper.hiv_result_datetime, self.subject_visit_male.report_datetime)
        self.assertEquals(subject_status_helper.new_pos, None)

        ahs_y2_subject_visit = self.ahs_y2_subject_visit()
        report_datetime = self.get_utcnow() + datetime.timedelta(3 * 365 / 12)
        self.make_requisition(ahs_y2_subject_visit, MICROTUBE, report_datetime)
        self.make_hivtesting_history(ahs_y2_subject_visit, report_datetime, NO, NO, None, NO)
        self.make_hiv_care_adherence(self.ahs_y2_subject_visit(), self.get_utcnow(), NO, YES, NO, YES, NO)

        self.make_hiv_result(POS, ahs_y2_subject_visit, report_datetime)
        subject_status_helper = SubjectStatusHelper(ahs_y2_subject_visit)
        self.assertEquals(subject_status_helper.hiv_result, POS)
        self.assertEquals(subject_status_helper.hiv_result_datetime, ahs_y2_subject_visit.report_datetime)
        self.assertEquals(subject_status_helper.new_pos, True)

    def tests_hiv_result5(self):
        """"""

        result_date = datetime(2014, 2, 9)
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, YES, POS, NO)
        self.make_hivtest_review(self.subject_visit_male, NEG, self.get_utcnow(), result_date)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertIsNone(subject_status_helper.hiv_result)

        subject_status_helper = SubjectStatusHelper(self.subject_visit_male_annual)
        self.assertIsNone(subject_status_helper.hiv_result)

    def tests_hiv_result4(self):
        """"""

        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, NO)
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, NO, YES)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.hiv_result, POS)

    def tests_on_arv1(self):
        """"""
        with transaction.atomic():
            self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, NO)
            self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, NO, YES)
            subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
            self.assertEquals(subject_status_helper.on_art, True)

    def tests_on_arv2(self):
        """"""
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, NO)
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, YES, YES)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.on_art, True)

    def tests_on_arv3(self):
        """"""
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, NO)
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, YES, NO)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.on_art, True)

    def tests_on_arv4(self):
        """"""

        self.startup()
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, NO)
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, NO, NO)
        subject_status_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEquals(subject_status_helper.on_art, False)

    def tests_hiv_result8(self):
        """Other record confirms a verbal positive as evidence of HIV infection not on ART."""

        self.requisition_metadata_obj(REQUIRED, T0, MICROTUBE, self.subject_visit_male.subject_identifier)

        self.assertEqual(
            1, self.requisition_metadata_obj(
                REQUIRED, T0, RESEARCH_BLOOD_DRAW, self.subject_visit_male.subject_identifier).count())

        self.assertEqual(
            1, self.requisition_metadata_obj(
                REQUIRED, T0, VIRAL_LOAD, self.subject_visit_male.subject_identifier).count())

    def tests_hiv_result6(self):
        """Other record confirms a verbal positive as evidence of HIV infection not on ART."""

        self.requisition_metadata_obj(REQUIRED, T0, MICROTUBE, self.subject_visit_male.subject_identifier)
        self.assertEqual(
            1, self.requisition_metadata_obj(
                NOT_REQUIRED, T0, RESEARCH_BLOOD_DRAW, self.subject_visit_male.subject_identifier).count())
        self.assertEqual(
            1, self.requisition_metadata_obj(
                NOT_REQUIRED, T0, VIRAL_LOAD, self.subject_visit_male.subject_identifier).count())

        # site_rule_groups.autodiscover()

        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, YES)
        subject_referral_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual(POS, subject_referral_helper.hiv_result)
        self.assertEqual(False, subject_referral_helper.new_pos)
        self.assertTrue(subject_referral_helper.on_art is None)

        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, NO, NO)
        subject_referral_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual(POS, subject_referral_helper.hiv_result)
        self.assertFalse(subject_referral_helper.new_pos)
        self.assertTrue(subject_referral_helper.on_art is False)

        hiv_result_documentation = mommy.make_recipe('bcpp_subject.hivresultdocumentation', subject_visit=self.subject_visit_male)

        subject_referral_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual(POS, subject_referral_helper.hiv_result)
        self.assertFalse(subject_referral_helper.new_pos)
        self.assertTrue(subject_referral_helper.on_art is False)
        self.assertEqual(hiv_result_documentation.result_date, subject_referral_helper.hiv_result_datetime.date())

        self.assertEqual(
            self.crf_metadata_obj(
                'bcpp_subject.hivresult', NOT_REQUIRED, T0, self.subject_visit_male.subject_identifier), 1)

        self.assertEqual(
            self.crf_metadata_obj(
                'bcpp_subject.pima', REQUIRED, T0, self.subject_visit_male.subject_identifier).count(), 1)

        self.assertEqual(
            1, self.requisition_metadata_obj(
                NOT_REQUIRED, T0, MICROTUBE, self.subject_visit_male.subject_identifier).count())

        self.assertEqual(
            1, self.requisition_metadata_obj(
                REQUIRED, T0, RESEARCH_BLOOD_DRAW, self.subject_visit_male.subject_identifier).count())

        self.assertEqual(
            1, self.requisition_metadata_obj(
                REQUIRED, T0, VIRAL_LOAD, self.subject_visit_male.subject_identifier).count())

    def tests_hiv_result7(self):
        """Other record confirms a verbal positive as evidence of HIV infection not on ART."""
        self.requisition_metadata_obj(REQUIRED, T0, MICROTUBE, self.subject_visit_male.subject_identifier)
        self.assertEqual(
            1, self.requisition_metadata_obj(NOT_REQUIRED, T0, RESEARCH_BLOOD_DRAW, self.subject_visit_male.subject_identifier))
        self.assertEqual(
            1, self.requisition_metadata_obj(NOT_REQUIRED, T0, VIRAL_LOAD, self.subject_visit_male.subject_identifier))

        # site_rule_groups.autodiscover()

        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, YES)
        subject_referral_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual(POS, subject_referral_helper.hiv_result)
        self.assertEqual(False, subject_referral_helper.new_pos)
        self.assertTrue(subject_referral_helper.on_art is None)

        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, YES, NO, YES, YES)
        subject_referral_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual(POS, subject_referral_helper.hiv_result)
        self.assertFalse(subject_referral_helper.new_pos)
        self.assertTrue(subject_referral_helper.on_art)

        hiv_result_documentation = mommy.make_recipe(
            'bcpp_subject.hivresultdocumentation', subject_visit=self.subject_visit_male,
            result_recorded=POS,
            result_date=self.hiv_test_date,
            result_doc_type='ART Prescription'
        )
        subject_referral_helper = SubjectStatusHelper(self.subject_visit_male)
        self.assertEqual(POS, subject_referral_helper.hiv_result)
        self.assertFalse(subject_referral_helper.new_pos)
        self.assertTrue(subject_referral_helper.on_art)

        self.assertEqual(
            self.crf_metadata_obj(
                'bcpp_subject.hivresult', NOT_REQUIRED, T0, self.subject_visit_male.subject_identifier), 1)

        self.assertEqual(
            self.crf_metadata_obj(
                'bcpp_subject.pima', NOT_REQUIRED, T0, self.subject_visit_male.subject_identifier).count(), 1)
        self.assertEqual(hiv_result_documentation.result_date, subject_referral_helper.hiv_result_datetime.date())

        self.requisition_metadata_obj(NOT_REQUIRED, T0, MICROTUBE, self.subject_visit_male.subject_identifier)
        self.assertEqual(
            1, self.requisition_metadata_obj(REQUIRED, T0, RESEARCH_BLOOD_DRAW, self.subject_visit_male.subject_identifier))
        self.assertEqual(
            1, self.requisition_metadata_obj(REQUIRED, T0, VIRAL_LOAD, self.subject_visit_male.subject_identifier))

 
#     def tests_hiv_result8(self):
#         """Other record confirms a verbal positive as evidence of HIV infection not on ART."""
#         self.startup()
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Microtube', entry_status=REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Research Blood Draw', entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Viral Load', entry_status=NOT_REQUIRED).count() == 1)
#         site_rule_groups.autodiscover()
#         HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='NEG', has_record='No', other_record='No')
#         self.assertTrue(ScheduledEntryMetaData.objects.filter(appointment=self.subject_visit_male.appointment, entry__model_name='hivresult', entry_status=REQUIRED).count() == 1)
#         self.assertTrue(ScheduledEntryMetaData.objects.filter(appointment=self.subject_visit_male.appointment, entry__model_name='pima', entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Microtube', entry_status=REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Research Blood Draw', entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Viral Load', entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Venous (HIV)', entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='ELISA', entry_status=NOT_REQUIRED).count() == 1)
#         site_rule_groups._registry = {}
 
#     def tests_hiv_result9(self):
#         """Other record confirms a verbal positive as evidence of HIV infection not on ART."""
#         self.startup()
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Microtube', entry_status=REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Research Blood Draw', entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Viral Load', entry_status=NOT_REQUIRED).count() == 1)
#         site_rule_groups.autodiscover()
#         HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result='NEG',
#                                  has_record='No', other_record='No')
#         self.assertTrue(ScheduledEntryMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment,
#             entry__model_name='hivresult', entry_status=REQUIRED).count() == 1)
#         self.assertTrue(ScheduledEntryMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment, entry__model_name='pima',
#             entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment,
#             lab_entry__requisition_panel__name='Microtube', entry_status=REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Research Blood Draw',
#             entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Viral Load',
#             entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment,
#             lab_entry__requisition_panel__name='Venous (HIV)', entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment,
#             lab_entry__requisition_panel__name='ELISA', entry_status=NOT_REQUIRED).count() == 1)
#         site_rule_groups._registry = {}
# 
# 
#     def tests_hiv_result10(self):
#         """Other record confirms a verbal positive as evidence of HIV infection not on ART."""
# 
#         self.assertTrue(RequisitionMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment,
#             lab_entry__requisition_panel__name='Microtube',
#             entry_status=REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment,
#             lab_entry__requisition_panel__name='Research Blood Draw',
#             entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment,
#             lab_entry__requisition_panel__name='Viral Load',
#             entry_status=NOT_REQUIRED).count() == 1)
#         self.startup()
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Microtube', entry_status=REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Research Blood Draw', entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Viral Load', entry_status=NOT_REQUIRED).count() == 1)
#         site_rule_groups.autodiscover()
#         HivTestingHistoryFactory(
#             subject_visit=self.subject_visit_male, verbal_hiv_result='NEG', has_record='No', other_record='No')
#         panel = Panel.objects.get(name='Microtube')
#         SubjectRequisitionFactory(
#             subject_visit=self.subject_visit_male, site=self.site_code, panel=panel,
#             aliquot_type=AliquotType.objects.get(alpha_code='WB'))
#         HivResultFactory(
#             subject_visit=self.subject_visit_male, hiv_result=POS, hiv_result_datetime=datetime.today(), )
#         self.assertTrue(ScheduledEntryMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment, entry__model_name='hicenrollment',
#             entry_status=NOT_REQUIRED).count() == 1)
#         self.assertTrue(ScheduledEntryMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment,
#             entry__model_name='hivresult', entry_status=KEYED).count() == 1)
#         self.assertTrue(ScheduledEntryMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment, entry__model_name='pima',
#             entry_status=REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Microtube',
#             entry_status=KEYED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment,
#             lab_entry__requisition_panel__name='Research Blood Draw', entry_status=REQUIRED).count() == 1)
#         self.assertTrue(RequisitionMetaData.objects.filter(
#             appointment=self.subject_visit_male.appointment, lab_entry__requisition_panel__name='Viral Load',
#             entry_status=REQUIRED).count() == 1)
#         site_rule_groups._registry = {}
