from django.contrib import admin

from edc_base.fieldsets import FormLabel
from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import HivLinkageToCareForm
from ..models import HivLinkageToCare, SubjectReferral
from .modeladmin_mixins import CrfModelAdminMixin


class CustomFormLabelMixin:

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


@admin.register(HivLinkageToCare, site=bcpp_subject_admin)
class HivLinkageToCareAdmin(CustomFormLabelMixin, CrfModelAdminMixin, admin.ModelAdmin):
    form = HivLinkageToCareForm

    fieldsets = (
        (None, {
            'fields': [
                "subject_visit",
                "report_datetime",
                "kept_appt",
                "different_clinic",
                "failed_attempt_date",
                "first_attempt_date",
                "evidence_referral",
                "evidence_referral_other",
                "recommended_art",
                "reason_recommended_art",
                "reason_recommended_art_other",
                "initiated",
                "initiated_date",
                "initiated_clinic",
                "initiated_clinic_community",
                "evidence_art",
                "evidence_art_other",
            ]}), audit_fieldset_tuple)

    radio_fields = {
        "kept_appt": admin.VERTICAL,
        "evidence_referral": admin.VERTICAL,
        "recommended_art": admin.VERTICAL,
        "reason_recommended_art": admin.VERTICAL,
        "initiated": admin.VERTICAL,
        "evidence_art": admin.VERTICAL}
