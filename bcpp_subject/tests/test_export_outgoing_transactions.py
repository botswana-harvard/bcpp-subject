from django.test import TestCase

from bcpp_subject.tests.test_mixins import SubjectMixin
from edc_sync.utils.export_outgoing_transactions import export_outgoing_transactions


class TestExportOutgoingTransactions(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.make_subject_visit_for_consented_subject_female('T0')

    def test_outgoing_transactions(self):
        """Assert correct number of transactions are exported to a json file"""

        transaction_count = export_outgoing_transactions(None)

        expected_count = (353, 353)
        self.assertTupleEqual(
            transaction_count,
            expected_count,
            "unxepected transaction count")
