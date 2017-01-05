from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from django.urls.base import reverse

from edc_admin_exclude.admin import AdminExcludeFieldsMixin
from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin)
from edc_visit_tracking.modeladmin_mixins import CrfModelAdminMixin as VisitTrackingCrfModelAdminMixin

from ..constants import BASELINE, ANNUAL
from ..models import SubjectVisit


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin, ModelAdminAuditFieldsMixin,
                      ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin, admin.ModelAdmin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


class CrfModelAdminMixin(VisitTrackingCrfModelAdminMixin, ModelAdminMixin):

    visit_model = 'bcpp_subject.subjectvisit'
    visit_attr = 'subject_visit'

    instructions = (
        'Please complete the questions below. Required questions are in bold. '
        'When all required questions are complete click SAVE. Based on your responses, additional questions may be '
        'required or some answers may need to be corrected.')

    def view_on_site(self, obj):
        member = obj.subject_visit.household_member
        return reverse(
            'bcpp-subject:dashboard_url', kwargs=dict(member=member.pk))


class SubjectAdminExcludeMixin(AdminExcludeFieldsMixin):

    visit_model = SubjectVisit
    visit_attr = 'subject_visit'
    visit_codes = {BASELINE: ['T0'], ANNUAL: ['T1', 'T2', 'T3']}
