from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..models import MedicalDiagnoses
from ..forms import MedicalDiagnosesForm
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(MedicalDiagnoses, site=bcpp_subject_admin)
class MedicalDiagnosesAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MedicalDiagnosesForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'diagnoses',
                'heart_attack_record',
                'cancer_record',
                'tb_record',
                'sti_record')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "heart_attack_record": admin.VERTICAL,
        "cancer_record": admin.VERTICAL,
        "tb_record": admin.VERTICAL,
        "sti_record": admin.VERTICAL, }

    filter_horizontal = ('diagnoses',)

    additional_instructions = mark_safe(
        "<H5>Note to Interviewer</H5>Please review the available OPD card "
        "or other medical records, for all participants. "
        "<H5><span style=\"color:orange;\">Read to Participant</span></H5>"
        "I am now going to ask you some questions about major illnesses "
        "that you may have had, (or if seen by us before, have had since we spoke "
        "with you at our last visit). Sometimes people "
        "call different sicknesses by different names. "
        "If you do not understand what I mean, please ask. "
        "<br>Also, please remember that your answers will be "
        "kept confidential.")
