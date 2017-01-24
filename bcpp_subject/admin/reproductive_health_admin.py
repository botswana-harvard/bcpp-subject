from django.contrib import admin
from django.utils.translation import ugettext as _

from edc_base.fieldsets import Remove

from ..admin_site import bcpp_subject_admin
from ..constants import T0
from ..forms import ReproductiveHealthForm
from ..models import ReproductiveHealth

from .modeladmin_mixins import CrfModelAdminMixin

fields = (
    "when_pregnant",
    "gestational_weeks",
    "pregnancy_hiv_tested",
    "pregnancy_hiv_retested")


@admin.register(ReproductiveHealth, site=bcpp_subject_admin)
class ReproductiveHealthAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = ReproductiveHealthForm

    conditional_fieldlist = {T0: Remove(fields)}

    fieldsets = (
        (None, {
            'fields': (
                "subject_visit",
                "number_children",
                "menopause",
                "family_planning",
                "family_planning_other",
                'currently_pregnant',
                'when_pregnant',
                'gestational_weeks',
                'pregnancy_hiv_tested',
                'pregnancy_hiv_retested')}),
    )

    radio_fields = {
        "menopause": admin.VERTICAL,
        "currently_pregnant": admin.VERTICAL,
        "when_pregnant": admin.VERTICAL,
        "pregnancy_hiv_tested": admin.VERTICAL,
        "pregnancy_hiv_retested": admin.VERTICAL
    }

    filter_horizontal = ("family_planning",)
    instructions = [("<h5>Note to Interviewer</h5> This section is to be"
                     " completed by female participants. SKIP for male participants."),
                    _("Read to Participant: I am now going to ask you questions"
                      " about reproductive health and pregnancy.")]
