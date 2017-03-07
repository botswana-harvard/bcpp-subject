from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import HivCareAdherenceForm
from ..models import HivCareAdherence
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivCareAdherence, site=bcpp_subject_admin)
class HivCareAdherenceAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'first_positive')}),
        ('Care', {
            'fields': (
                'medical_care',
                'no_medical_care',
                'no_medical_care_other',
                'ever_recommended_arv',
                'ever_taken_arv',
                'why_no_arv',
                'why_no_arv_other')}),
        ('Antiretiroviral Therapy', {
            'fields': (
                'on_arv',
                'arv_evidence',
                'first_arv',
                'arv_stop_date',
                'arv_stop',
                'arv_stop_other',
                'arvs',
                'arv_other',
                'is_first_regimen',
                'prev_switch_date',
                'prev_arvs',
                'prev_arv_other',
            )}),
        ('Adherence', {
            'fields': (
                'adherence_4_day',
                'adherence_4_wk'
            )}),
        ('Hospitalization', {
            'fields': (
                'hospitalized_art_start',
                'hospitalized_art_start_duration',
                'hospitalized_art_start_reason',
                'hospitalized_art_start_reason_other',
                'chronic_disease',
                'medication_toxicity',
                'hospitalized_evidence',
                'hospitalized_evidence_other')}),
        ('Clinic', {
            'fields': (
                'clinic_receiving_from',
                'next_appointment_date')}),
        audit_fieldset_tuple,
    )

    form = HivCareAdherenceForm

    radio_fields = {
        'medical_care': admin.VERTICAL,
        'no_medical_care': admin.VERTICAL,
        'ever_recommended_arv': admin.VERTICAL,
        'ever_taken_arv': admin.VERTICAL,
        'why_no_arv': admin.VERTICAL,
        'on_arv': admin.VERTICAL,
        'arv_stop': admin.VERTICAL,
        'adherence_4_day': admin.VERTICAL,
        'adherence_4_wk': admin.VERTICAL,
        'arv_evidence': admin.VERTICAL,
        'is_first_regimen': admin.VERTICAL,
        'hospitalized_art_start': admin.VERTICAL,
        'hospitalized_art_start_reason': admin.VERTICAL,
        'hospitalized_evidence': admin.VERTICAL,
    }

    filter_horizontal = ('arvs', 'prev_arvs')

    additional_instructions = mark_safe(
        'This section is only to be completed by HIV-positive participants '
        'who knew that they were HIV-positive before today. '
        'Section should be skipped for HIV-negative participants '
        'and participants who first tested HIV-positive today.'
        '<H5><span style="color:orange;">Read to Participant</span></H5>'
        'I am now going to ask you some questions about care you may have '
        'been given for your HIV infection.')

    list_display = (
        'subject_visit',
        'on_arv',
        'arv_evidence',
        'ever_taken_arv',
    )

    list_filter = (
        'on_arv',
        'arv_evidence',
        'ever_taken_arv',
    )
