from django.test import TestCase
from django.test.utils import tag

from bcpp_subject.models.appointment import Appointment
from bcpp_subject.models.subject_consent import SubjectConsent
from bcpp_subject.models.subject_visit import SubjectVisit
from bcpp_subject.tests.test_mixins import SubjectMixin

from edc_metadata.models import CrfMetadata, RequisitionMetadata
from edc_sync.models import OutgoingTransaction, IncomingTransaction

from household.models.household import Household
from household.models.household_log import HouseholdLog
from household.models.household_log_entry import HouseholdLogEntry
from household.models.household_structure.household_structure import HouseholdStructure

from member.models.enrollment_checklist import EnrollmentChecklist
from member.models.household_head_eligibility import HouseholdHeadEligibility
from member.models.household_member.household_member import HouseholdMember
from member.models.representative_eligibility import RepresentativeEligibility
from plot.models import Plot, PlotLog, PlotLogEntry


@tag('TestConsumeIncomingTransactions')
class TestConsumeIncomingTransactions(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()

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

    def test_created_incoming_tx(self):
        total_outgoing_transactions = OutgoingTransaction.objects.all().count()
        for outgoing in OutgoingTransaction.objects.all():
            data = outgoing.__dict__
            del data['using']
            del data['is_consumed_middleman']
            del data['is_consumed_server']
            del data['_state']
            del data['hostname_modified']
            IncomingTransaction.objects.create(**data)
        self.assertEqual(
            total_outgoing_transactions,
            IncomingTransaction.objects.all().count())

    @tag('test_created_incoming_tx')
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

    @tag('test_consume_incoming_transactions_enrollment_models')
    def test_consume_incoming_transactions_enrollment_models(self):
        self.delete_enrollment_records()
        for outgoing in OutgoingTransaction.objects.filter(
                tx_name__in=[
                    'plot.plot', 'plot.plotlog', 'plot.plotlogentry',
                    'household.household', 'household.householdlog',
                    'household.householdstructure',
                    'member.householdmember', 'household.householdlogentry',
                    'household.householdheadeligibility',
                    'member.representativeeligibility',
                    # 'member.enrollmentchecklist',
                    # 'bcpp_subject.appointment', 'bcpp_subject.subjectvisit',
                ]).order_by('created'):  # , 'plot.plotlogentry'
            data = outgoing.__dict__
            del data['using']
            del data['is_consumed_middleman']
            del data['is_consumed_server']
            del data['_state']
            del data['hostname_modified']
            IncomingTransaction.objects.create(**data)
        outgoing_tx = OutgoingTransaction.objects.all()
        outgoing_tx.delete()
        self.assertEqual(0, OutgoingTransaction.objects.all().count())

        for incoming_tx in IncomingTransaction.objects.filter(
                is_consumed=False, is_ignored=False, action='I').order_by('created'):
            incoming_tx.deserialize_transaction(check_hostname=False)

        self.assertNotEqual(0, HouseholdLogEntry.objects.all().count())
        self.assertNotEqual(0, HouseholdLog.objects.all().count())
#         self.assertNotEqual(0, SubjectVisit.objects.all().count())
#         self.assertNotEqual(0, Appointment.objects.all().count())
#         self.assertNotEqual(0, EnrollmentChecklist.objects.all().count())
#         self.assertNotEqual(0, RepresentativeEligibility.objects.all().count())
#         self.assertNotEqual(0, HouseholdHeadEligibility.objects.all().count())
        self.assertNotEqual(0, HouseholdMember.objects.all().count())
        self.assertNotEqual(0, HouseholdStructure.objects.all().count())
        self.assertNotEqual(0, Household.objects.all().count())
        self.assertNotEqual(0, PlotLogEntry.objects.all().count())
        self.assertNotEqual(0, PlotLog.objects.all().count())
        self.assertNotEqual(0, Plot.objects.all().count())
