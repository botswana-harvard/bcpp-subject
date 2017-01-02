from django.apps import apps as django_apps
from django.test import TestCase

from edc_sync.test_mixins import SyncTestSerializerMixin
from ..sync_models import sync_models
# from bcpp_subject

from .test_mixins import CompleteCrfsMixin
from edc_sync.models import OutgoingTransaction


class TestNaturalKey(SyncTestSerializerMixin, CompleteCrfsMixin, TestCase):

    def test_natural_key_attrs(self):
        self.sync_test_natural_key_attr('bcpp_subject')

    def test_get_by_natural_key_attr(self):
        self.sync_test_get_by_natural_key_attr('bcpp_subject')

    def test_enrollment_models(self):
        """bcpp_subject.subjectconsent,  bcpp_subject.enrollment, bcpp_subject.subjectvisit"""
        verbose = False
        self.make_subject_visit_for_consented_subject(visit_code='T0')
        model_objs = []
        completed_model_objs = {}
        completed_model_lower = []
        for outgoing_transaction in OutgoingTransaction.objects.all():
            if outgoing_transaction.tx_name in sync_models:
                model_cls = django_apps.get_app_config('bcpp_subject').get_model(
                    outgoing_transaction.tx_name.split('.')[1])
                obj = model_cls.objects.get(pk=outgoing_transaction.tx_pk)
                if outgoing_transaction.tx_name in completed_model_lower:
                    continue
                model_objs.append(obj)
                completed_model_lower.append(outgoing_transaction.tx_name)
        completed_model_objs.update({'bcpp_subject': model_objs})
        self.sync_test_natural_keys(completed_model_objs, verbose=verbose)

    def test_crf_models(self):
        """ """
#         self.complete_crfs(      , visit, visit_attr, entry_status, subject_identifier)
        subject_visit = self.make_subject_visit_for_consented_subject(visit_code='T0')
        verbose = False
        visits = ['T0']
        subject_visits = self.add_subject_visits(*visits, subject_identifier=subject_visit.subject_identifier)
        self.sync_test_natural_keys_by_schedule(
            visits=subject_visits,
            verbose=verbose,
            visit_attr='subject_visit'
        )
