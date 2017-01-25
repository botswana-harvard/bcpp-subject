from django.contrib import admin
from django.utils.translation import ugettext as _


from edc_base.fieldsets import Fieldset

from ..admin_site import bcpp_subject_admin
from ..forms import EducationForm
from ..models import Education
from ..constants import T1, T2, T3, E0

from .modeladmin_mixins import CrfModelAdminMixin
from edc_base.modeladmin_mixins import audit_fieldset_tuple

education_fields = (
    'education',
    'working',
    'job_type',
    'reason_unemployed')


@admin.register(Education, site=bcpp_subject_admin)
class EducationAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = EducationForm

    conditional_fieldsets = {
        T1: Fieldset(*education_fields, section='Education'),
        T2: Fieldset(*education_fields, section='Education'),
        T3: Fieldset(*education_fields, section='Education'),
        E0: Fieldset(*education_fields, section='Education'),
    }

    fieldsets = (
        ('Employment', {
            'fields': (
                "subject_visit",
                'job_description',
                'monthly_income'),
        }),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "education": admin.VERTICAL,
        "working": admin.VERTICAL,
        'job_type': admin.VERTICAL,
        'reason_unemployed': admin.VERTICAL,
        'job_description': admin.VERTICAL,
        "monthly_income": admin.VERTICAL,
        'job_description': admin.VERTICAL,
        "monthly_income": admin.VERTICAL, }

    instructions = [_("<H5>Read to Participant</H5> Next, I will ask you some "
                      "questions about what education and work you "
                      "may have done or are currently doing.")]
