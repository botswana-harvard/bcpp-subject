from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..models import Appointment

from ..admin_site import bcpp_subject_admin


@admin.register(Appointment, site=bcpp_subject_admin)
class AppointmentAdmin(ModelAdminMixin):

    fieldsets = (
        (None, {
            'fields': [
                'appt_datetime',
                'appt_type',
                'appt_status',
                'appt_reason',
                'comment',
            ]}), audit_fieldset_tuple)

    radio_fields = {
        'appt_type': admin.VERTICAL,
        'appt_status': admin.VERTICAL}
