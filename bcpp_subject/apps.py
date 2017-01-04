from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = 'bcpp_subject'
    list_template_name = None

    def ready(self):
        from bcpp_subject.models.signals import subject_consent_on_post_save
