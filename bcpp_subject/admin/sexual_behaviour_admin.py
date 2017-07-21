from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_base.fieldsets import Remove, FormLabel
from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_constants.constants import YES
from bcpp_visit_schedule.constants import T0

from ..admin_site import bcpp_subject_admin
from ..forms import SexualBehaviourForm
from ..models import SexualBehaviour

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SexualBehaviour, site=bcpp_subject_admin)
class SexualBehaviourAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SexualBehaviourForm

    conditional_fieldlists = {
        T0: Remove('first_sex_partner_age', 'first_sex_partner_age_other'),
    }

    custom_form_labels = [
        FormLabel(
            field='ever_sex',
            label=('In your lifetime, have you ever had sex with anyone?<br>'
                   '<span style="color:orange;">Interviewer</span>. '
                   '<span style="font-weight:normal;">On {previous} subject '
                   'reported <B>YES</B>. Select <B>YES</B> to continue.</span>'),
            callback=lambda obj, appointment: True if obj.ever_sex == YES else False)
    ]

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'ever_sex',
                'lifetime_sex_partners',
                'last_year_partners',
                'more_sex',
                'first_sex',
                'first_sex_partner_age',
                'first_sex_partner_age_other',
                'condom',
                'alcohol_sex',)}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'ever_sex': admin.VERTICAL,
        'more_sex': admin.VERTICAL,
        'condom': admin.VERTICAL,
        'first_sex_partner_age': admin.VERTICAL,
        'alcohol_sex': admin.VERTICAL}

    additional_instructions = mark_safe(
        '<H5><span style="color:orange;">Read to Participant</span></H5>'
        'In this part of the interview, '
        'I will be asking you some questions about your '
        'sexual relationships that you might have had, '
        'and about sexual practices that you might have '
        'engaged in. Please let me know if you feel '
        'comfortable answering these questions now or if '
        'we should move to a different location. '
        'Some of these questions may make you feel uncomfortable; '
        'however, it is really important for us to get the '
        'most honest answer that you can give us. Please '
        'remember that all of your answers are confidential.')
