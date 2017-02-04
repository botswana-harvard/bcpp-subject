from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..models import SubjectReferral
from ..forms import SubjectReferralForm
from ..filters import SubjectCommunityListFilter, SubjectReferralIsReferredListFilter

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SubjectReferral, site=bcpp_subject_admin)
class SubjectReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SubjectReferralForm

    date_hierarchy = 'referral_appt_date'

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'report_datetime',
                'subject_referred',
                'scheduled_appt_date',
                'referral_appt_comment',
                'comment')}),
        audit_fieldset_tuple,
    )

    search_fields = ['subject_visit__appointment__registered_subject__first_name',
                     'subject_visit__appointment__registered_subject__subject_identifier']

    list_display = [
        'subject_visit',
        'report_datetime',
        'subject_referred',
        'referral_code',
        'referral_clinic_type',
        'referral_appt_date',
        'in_clinic_flag',
    ]

    list_filter = [
        # 'exported',
        'in_clinic_flag',
        SubjectReferralIsReferredListFilter,
        SubjectCommunityListFilter,
        'referral_code', 'report_datetime', 'referral_appt_date',
        'hostname_created']

    radio_fields = {
        "referral_code": admin.VERTICAL,
        "subject_referred": admin.VERTICAL,
        "referral_appt_comment": admin.VERTICAL,
    }
