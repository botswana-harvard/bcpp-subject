from django.apps import AppConfig as DjangoApponfig
from django.conf import settings


class AppConfig(DjangoApponfig):
    name = 'bcpp_subject'
    listboard_template_name = 'bcpp_subject/listboard.html'
    dashboard_template_name = 'bcpp_subject/dashboard.html'
    base_template_name = 'edc_base/base.html'
    listboard_url_name = 'bcpp_subject_dashboard:listboard_url'
    anonymous_listboard_url_name = 'bcpp_subject_dashboard:anonymous_listboard_url'
    dashboard_url_name = 'bcpp_subject_dashboard:dashboard_url'
    anonymous_dashboard_url_name = 'bcpp_subject_dashboard:anonymous_dashboard_url'
    admin_site_name = 'bcpp_subject_admin'

    def ready(self):
        from bcpp_subject.models.signals import (
            consent_on_post_save,
            subject_consent_on_post_delete,
            enrollment_checklist_anonymous_on_post_save,
            enrollment_checklist_anonymous_on_post_delete,
            enrollment_checklist_on_post_delete,
            enrollment_checklist_on_post_save,
            referral_on_post_save)


if settings.APP_NAME == 'bcpp_subject':

    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_appointment.facility import Facility
    from edc_device.device_permission import DevicePermissions
    from edc_device.device_permission import DeviceAddPermission, DeviceChangePermission
    from edc_device.constants import CENTRAL_SERVER, CLIENT, NODE_SERVER
    from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
    from edc_map.apps import AppConfig as BaseEdcMapAppConfig
    from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig

    class EdcMapAppConfig(BaseEdcMapAppConfig):
        verbose_name = 'Test Mappers'
        mapper_model = 'plot.plot'
        landmark_model = []
        verify_point_on_save = False
        zoom_levels = ['14', '15', '16', '17', '18']
        identifier_field_attr = 'plot_identifier'
        extra_filter_field_attr = 'enrolled'

    class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
        use_settings = True
        device_permissions = DevicePermissions(
            DeviceAddPermission(
                model='plot.plot',
                device_roles=[CENTRAL_SERVER, CLIENT]),
            DeviceChangePermission(
                model='plot.plot',
                device_roles=[NODE_SERVER, CENTRAL_SERVER, CLIENT]))

    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'bcpp_subject': ('subject_visit', 'bcpp_subject.subjectvisit')}

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        app_label = 'bcpp_subject'
        default_appt_type = 'home'
        facilities = {
            'home': Facility(name='home', days=[MO, TU, WE, TH, FR, SA, SU],
                             slots=[99999, 99999, 99999, 99999, 99999, 99999, 99999])}
