from django.contrib import admin

from edc_base.fieldsets import FormLabel
from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_constants.constants import NO

from ..admin_site import bcpp_subject_admin
from ..forms import HivLinkageToCareForm
from ..models import HivLinkageToCare, SubjectReferral

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivLinkageToCare, site=bcpp_subject_admin)
class HivLinkageToCareAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = HivLinkageToCareForm

    custom_form_labels = [
        FormLabel(
            field='kept_appt',
            label=(
                'When we last saw you in {previous} we scheduled an appointment '
                'for you in an HIV care clinic on {referral_appt_date}. '
                'Did you keep that appointment?'),
            previous_appointment=True)
    ]

    def format_form_label(self, label=None, instance=None, appointment=None, **kwargs):
        referral_appt_date = '(date unknown)'
        previous = appointment.appt_datetime.strftime('%B %Y')
        try:
            subject_referral = SubjectReferral.objects.get(
                subject_visit=appointment.visit)
        except SubjectReferral.DoesNotExist:
            pass
        else:
            if subject_referral.referral_appt_date:
                referral_appt_date = subject_referral.referral_appt_date.strftime(
                    '%Y-%m-%d')
        label = label.format(
            previous=previous, referral_appt_date=referral_appt_date)
        return label

    fieldsets = (
        (None, {
            'fields': [
                "subject_visit",
                "report_datetime",
                "kept_appt",
                "diff_clininc",
                "left_clininc_datetime",
                "clinic_first_datetime",
                "evidence_type_clinic",
                "evidence_type_clinic_other",
                "recommended_therapy",
                "reason_recommended",
                "reason_recommended_other",
                "startered_therapy",
                "startered_therapy_date",
                "start_therapy_clininc",
                "start_therapy_clininc_other",
                "not_refered_clininc",
                "evidence_not_refered",
                "evidence_not_refered_other",
            ]}), audit_fieldset_tuple)

    radio_fields = {
        "kept_appt": admin.VERTICAL,
        "evidence_type_clinic": admin.VERTICAL,
        "recommended_therapy": admin.VERTICAL,
        "reason_recommended": admin.VERTICAL,
        "startered_therapy": admin.VERTICAL,
        "start_therapy_clininc": admin.VERTICAL,
        "evidence_not_refered": admin.VERTICAL}
