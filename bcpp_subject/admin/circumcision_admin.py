from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_base.fieldsets import FormLabel
from edc_constants.constants import NO

from ..admin_site import bcpp_subject_admin
from ..forms import CircumcisionForm
from ..models import Circumcision
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Circumcision, site=bcpp_subject_admin)
class CircumcisionAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CircumcisionForm

    custom_form_labels = [
        FormLabel(
            field='circumcised',
            label='Since we last saw you in {previous}, were you circumcised?',
            callback=lambda obj, appointment: True if obj.circumcised == NO else False)
    ]

    fieldsets = (
        (None, {
            'fields': [
                'subject_visit',
                'circumcised',
                'circumcised_location',
                'circumcised_location_other',
            ]}), audit_fieldset_tuple)

    radio_fields = {
        'circumcised': admin.VERTICAL,
        'circumcised_location': admin.VERTICAL}

    additional_instructions = mark_safe(
        '<H5><span style="color:orange;">Read to Participant</span></H5>'
        'Some men are circumcised. Male circumcision is '
        '[enter site specific word] when the foreskin of the man\'s penis '
        'has been cut off. I would like to ask you a few questions regarding '
        'male circumcision.')
