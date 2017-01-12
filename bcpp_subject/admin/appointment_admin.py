from django.contrib import admin


from .modeladmin_mixins import ModelAdminMixin

from ..models import Appointment

from ..admin_site import bcpp_subject_admin


@admin.register(Appointment, site=bcpp_subject_admin)
class AppointmentAdmin(ModelAdminMixin):

    fields = (
        'appt_datetime',
        'appt_type',
        'appt_status',
        'appt_reason',
        'comment',
    )

    radio_fields = {
        'appt_type': admin.VERTICAL,
        'appt_status': admin.VERTICAL}
