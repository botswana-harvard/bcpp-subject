from django.apps import AppConfig as DjangoApponfig


class AppConfig(DjangoApponfig):
    name = 'bcpp_subject'
    listboard_template_name = 'bcpp_subject/listboard.html'
    listboard_url_name = 'bcpp-subject:listboard_url'
    dashboard_url_name = 'bcpp-subject:dashboard_url'
    url_namespace = 'bcpp-subject'
    admin_site_name = 'bcpp_subject_admin'

    def ready(self):
        from bcpp_subject.models.signals import subject_consent_on_post_save
