from django.apps import apps as django_apps
from django.test import TestCase

from edc_sync.test_mixins import SyncTestSerializerMixin
from ..sync_models import sync_models

from .test_mixins import CompleteCrfsMixin, SubjectMixin
from edc_sync.models import OutgoingTransaction
from django.test.utils import tag
from ..constants import E0


class TestNaturalKey(SyncTestSerializerMixin, SubjectMixin, CompleteCrfsMixin, TestCase):

    @tag('natural_key')
    def test_natural_key_attrs(self):
        self.sync_test_natural_key_attr('bcpp_subject')

    @tag('natural_key')
    def test_get_by_natural_key_attr(self):
        self.sync_test_get_by_natural_key_attr('bcpp_subject')

    @tag('natural_key')
    def test_enrollment_models(self):
        """bcpp_subject.subjectconsent,  bcpp_subject.enrollment, bcpp_subject.subjectvisit"""
        verbose = False
        consent_data_male = {
            'identity': '31721515',
            'confirm_identity': '31721515',
        }
        survey_schedule = self.get_survey_schedule(index=2)
        self.make_subject_visit_for_consented_subject_male(
            E0, survey_schedule=survey_schedule, **consent_data_male)
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

    @tag('natural_key')
    def test_crf_models(self):
        """ """
        consent_data_male = {
            'identity': '31721515',
            'confirm_identity': '31721515',
        }
        survey_schedule = self.get_survey_schedule(index=2)
        subject_visit = self.make_subject_visit_for_consented_subject_male(
            E0, survey_schedule=survey_schedule, **consent_data_male)
        verbose = False
        self.sync_test_natural_keys_by_schedule(
            visits=[subject_visit],
            verbose=verbose,
            visit_attr='subject_visit'
        )
