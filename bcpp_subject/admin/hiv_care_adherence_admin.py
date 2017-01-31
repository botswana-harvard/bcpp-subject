from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_base.fieldsets import Fieldset, Insert

from ..admin_site import bcpp_subject_admin
from ..constants import T1, T2, T3, E0
from ..forms import HivCareAdherenceForm
from ..models import HivCareAdherence

from .modeladmin_mixins import CrfModelAdminMixin


hospitalization_fieldset = Fieldset(
    'hospitalized_art_start',
    'hospitalized_art_start_duration',
    'hospitalized_art_start_reason',
    'hospitalized_reason_evidence',
    'hospitalized_reason_evidence_other',
    section='Hospitalization')

insert_regimen_fields = Insert(
    ('regimen_currently_prescribed',
     'first_regimen',
     'hospitalized_art_start_reason',
     'hospitalized_art_start_reason_other',
     'chronic_diseases',
     'medication_toxicity',
     ),
    after='arv_evidence')


@admin.register(HivCareAdherence, site=bcpp_subject_admin)
class HivCareAdherenceAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    conditional_fieldsets = {
        E0: hospitalization_fieldset
    }

    conditional_fieldlists = {
        T1: insert_regimen_fields,
        T2: insert_regimen_fields,
        T3: insert_regimen_fields,
        E0: insert_regimen_fields,
    }

    filter_horizontal = ('hospitalization_reason', 'hospitalization_reason')

    fieldsets = (
        (None, {
            'fields': (
                "subject_visit",
                "first_positive",
                "medical_care",
                "no_medical_care",
                "no_medical_care_other",
                'ever_recommended_arv',
                'ever_taken_arv',
                'why_no_arv',
                'why_no_arv_other',
                'first_arv',
                'on_arv',
                'arv_evidence',
                'clinic_receiving_from',
                'next_appointment_date',
                'arv_stop_date',
                'arv_stop',
                'arv_stop_other',
                'adherence_4_day',
                'adherence_4_wk')}),
        audit_fieldset_tuple,
    )

    form = HivCareAdherenceForm

    radio_fields = {
        "medical_care": admin.VERTICAL,
        "no_medical_care": admin.VERTICAL,
        "ever_recommended_arv": admin.VERTICAL,
        "ever_taken_arv": admin.VERTICAL,
        "why_no_arv": admin.VERTICAL,
        "on_arv": admin.VERTICAL,
        "arv_stop": admin.VERTICAL,
        "adherence_4_day": admin.VERTICAL,
        "adherence_4_wk": admin.VERTICAL,
        "arv_evidence": admin.VERTICAL,
        'first_regimen': admin.VERTICAL,
        "first_regimen": admin.VERTICAL,
        'hospitalized_art_start': admin.VERTICAL,
        'hospitalized_reason_evidence': admin.VERTICAL,
    }

    filter_horizontal = (
        'regimen_currently_prescribed',
        'hospitalized_art_start_reason',
    )

    instructions = [("Note to Interviewer: This section is only to be"
                     " completed by HIV-positive participants who knew"
                     " that they were HIV-positive before today."
                     " Section should be skipped for HIV-negative participants"
                     " and participants who first tested HIV-positive"
                     " today. Read to Participant: I am now going to"
                     " ask you some questions about care you may have"
                     " been given for your HIV infection.")]
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
