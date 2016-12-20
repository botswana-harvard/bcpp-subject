from django.apps import AppConfig as DjangoApponfig
from edc_visit_tracking.apps import AppConfig as EdcVisitTrackingAppConfigParent


class AppConfig(DjangoApponfig):
    name = 'bcpp_subject'

    def ready(self):
        from bcpp_subject.models.signals import (
            subject_consent_on_post_save, update_or_create_registered_subject_on_post_save,
            update_subject_referral_on_post_save)


class EdcVisitTrackingAppConfig(EdcVisitTrackingAppConfigParent):
    visit_models = {'bcpp_subject': ('subject_visit', 'bcpp_subject.subjectvisit')}
