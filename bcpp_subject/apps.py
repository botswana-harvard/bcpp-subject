from django.apps import AppConfig as DjangoApponfig

from edc_lab.apps import AppConfig as EdcLabAppConfig
from edc_visit_tracking.apps import AppConfig as EdcVisitTrackingAppConfigParent


class AppConfig(DjangoApponfig):
    name = 'bcpp_subject'
    list_template_name = None

    def ready(self):
        from bcpp_subject.models.signals import subject_consent_on_post_save


class EdcVisitTrackingAppConfig(EdcVisitTrackingAppConfigParent):
    visit_models = {'bcpp_subject': ('subject_visit', 'bcpp_subject.subjectvisit'),
                    'bcpp_lab': ('subject_visit', 'bcpp_subject.subjectvisit'), }


class EdcLabAppConfig(EdcLabAppConfig):
    app_label = 'bcpp_subject'
    requisition = 'bcpp_lab.subjectrequisition'
