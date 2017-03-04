from django.test import TestCase

from bcpp_subject.models.appointment import Appointment
from bcpp_subject.models.subject_consent import SubjectConsent
from bcpp_subject.models.subject_visit import SubjectVisit
from bcpp_subject.tests.test_mixins import SubjectMixin

from edc_metadata.models import CrfMetadata, RequisitionMetadata
from edc_sync.models import OutgoingTransaction, IncomingTransaction
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from household.models.household import Household
from household.models.household_log import HouseholdLog
from household.models.household_log_entry import HouseholdLogEntry
from household.models.household_structure.household_structure import HouseholdStructure

from member.models.enrollment_checklist import EnrollmentChecklist
from member.models.household_head_eligibility import HouseholdHeadEligibility
from member.models.household_member.household_member import HouseholdMember
from member.models.representative_eligibility import RepresentativeEligibility
from plot.models import Plot, PlotLog, PlotLogEntry
from edc_sync.test_mixins import SyncTestSerializerMixin

from .test_mixins import CompleteCrfsMixin


from django.conf import settings
from django.core.files import File
from model_mommy import mommy

from bcpp_subject.tests.test_mixins import SubjectMixin
from edc_sync.utils.export_outgoing_transactions import export_outgoing_transactions


class TestConsumeIncomingTransactions(
        SyncTestSerializerMixin, SubjectMixin, CompleteCrfsMixin, TestCase):

    def setUp(self):
        super().setUp()

    def get_transaction_file(self, transaction_path):
        path = (settings.MEDIA_ROOT + transaction_path)
        f = open(path)
        djangoFile = File(f)

        return djangoFile

    def delete_crfs(self, subject_visit):
        deleted_crfs = []
        for crf in site_visit_schedules.get_schedule('ess_schedule').visit_registry['E0'].crfs:
            try:
                Crf = crf.model
                crf = crf.model.objects.get(subject_visit=subject_visit)
                deleted_crfs.append(crf)
                crf.delete()
            except Crf.DoesNotExist:
                pass
        return deleted_crfs

    def delete_enrollment_records(self):
        subject_visits = SubjectVisit.objects.all()
        self.delete_audit_records(subject_visits)
        subject_visits.delete()
        appointments = Appointment.objects.all()
        self.delete_audit_records(appointments)
        appointments.delete()
        consents = SubjectConsent.objects.all()
        self.delete_audit_records(consents)
        consents.delete()
        enrollment_checklist = EnrollmentChecklist.objects.all()
        self.delete_audit_records(enrollment_checklist)
        enrollment_checklist.delete()
        household_head_eligibility = HouseholdHeadEligibility.objects.all()
        self.delete_audit_records(enrollment_checklist)
        household_head_eligibility.delete()
        representative_eligibility = RepresentativeEligibility.objects.all()
        self.delete_audit_records(representative_eligibility)
        representative_eligibility.delete()
        household_members = HouseholdMember.objects.all()
        self.delete_audit_records(household_members)
        household_members.delete()
        householdlog_entries = HouseholdLogEntry.objects.all()
        self.delete_audit_records(householdlog_entries)
        householdlog_entries.delete()
        household_logs = HouseholdLog.objects.all()
        self.delete_audit_records(household_logs)
        household_logs.delete()
        household_structures = HouseholdStructure.objects.all()
        self.delete_audit_records(household_structures)
        household_structures.delete()
        households = Household.objects.all()
        self.delete_audit_records(households)
        households.delete()
        plotLog_entry = PlotLogEntry.objects.all()
        self.delete_audit_records(plotLog_entry)
        plotLog_entry.delete()
        plot_logs = PlotLog.objects.all()
        self.delete_audit_records(plot_logs)
        plot_logs.delete()
        plots = Plot.objects.all()
        self.delete_audit_records(plots)
        plots.delete()
        crfs = CrfMetadata.objects.all()
        crfs.delete()
        reqs = RequisitionMetadata.objects.all()
        reqs.delete()

    def delete_audit_records(self, model_objs):
        for obj in model_objs:
            obj.history.all().delete()

    def test_crfs_incoming_transactions_bhs(self):
        self.make_subject_visit_for_consented_subject_male('T0')

        file_path = '/bcpp_otse_201702252025.json'

        export_outgoing_transactions(
            settings.MEDIA_ROOT + file_path)

        mommy.make_recipe(
            'edc_sync_files.transaction',
            transaction_file=self.get_transaction_file(file_path),
            consume=True,
        )

        client_crfs = self.delete_crfs(subject_visit=self.subject_visit_male_t0)
        self.delete_enrollment_records()

        for crf in client_crfs:
            Crf = crf.__class__
            try:
                Crf.objects.get(subject_visit=self.subject_visit_male_t0)
                self.fail("make sure all crfs are deleted!")
            except Crf.DoesNotExist:
                pass

        for incoming_tx in IncomingTransaction.objects.filter(
                is_consumed=False, is_ignored=False):
            incoming_tx.deserialize_transaction(check_hostname=False)

        for crf in client_crfs:
            Crf = crf.__class__
            try:
                self.assertTrue(Crf.objects.get(subject_visit=self.subject_visit_male_t0))
            except Crf.DoesNotExist:
                self.fail("Failed to sync and consume all models! Got {}".format(Crf._meta.model_name))

    def test_delete_enrollment_records(self):
        self.delete_enrollment_records()
        self.assertEqual(0, HouseholdLogEntry.objects.all().count())
        self.assertEqual(0, HouseholdLog.objects.all().count())
        self.assertEqual(0, SubjectVisit.objects.all().count())
        self.assertEqual(0, Appointment.objects.all().count())
        self.assertEqual(0, EnrollmentChecklist.objects.all().count())
        self.assertEqual(0, RepresentativeEligibility.objects.all().count())
        self.assertEqual(0, HouseholdHeadEligibility.objects.all().count())
        self.assertEqual(0, HouseholdMember.objects.all().count())
        self.assertEqual(0, HouseholdStructure.objects.all().count())
        self.assertEqual(0, Household.objects.all().count())
        self.assertEqual(0, PlotLogEntry.objects.all().count())
        self.assertEqual(0, PlotLog.objects.all().count())
        self.assertEqual(0, Plot.objects.all().count())

    def test_consume_incoming_transactions_enrollment_models(self):
        self.make_subject_visit_for_consented_subject_female('T0')

        file_path = '/bcpp_otse_201702252025.json'

        export_outgoing_transactions(
            settings.MEDIA_ROOT + file_path)

        mommy.make_recipe(
            'edc_sync_files.transaction',
            transaction_file=self.get_transaction_file(file_path),
            consume=True,
        )
        self.delete_enrollment_records()

        for incoming_tx in IncomingTransaction.objects.filter(
                is_consumed=False, is_ignored=False):
            incoming_tx.deserialize_transaction(check_hostname=False)

        self.assertNotEqual(0, HouseholdLogEntry.objects.all().count())
        self.assertNotEqual(0, HouseholdLog.objects.all().count())
        self.assertNotEqual(0, SubjectVisit.objects.all().count())
        self.assertNotEqual(0, Appointment.objects.all().count())
        self.assertNotEqual(0, EnrollmentChecklist.objects.all().count())
        self.assertNotEqual(0, RepresentativeEligibility.objects.all().count())
        self.assertNotEqual(0, HouseholdHeadEligibility.objects.all().count())
        self.assertNotEqual(0, HouseholdMember.objects.all().count())
        self.assertNotEqual(0, HouseholdStructure.objects.all().count())
        self.assertNotEqual(0, Household.objects.all().count())
        self.assertNotEqual(0, PlotLogEntry.objects.all().count())
        self.assertNotEqual(0, PlotLog.objects.all().count())
        self.assertNotEqual(0, Plot.objects.all().count())
