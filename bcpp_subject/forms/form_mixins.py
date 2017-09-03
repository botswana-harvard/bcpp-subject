from django import forms
from edc_base.modelform_mixins import JSONModelFormMixin
from edc_base.modelform_validators import FormValidatorMixin
from edc_visit_tracking.modelform_mixins import VisitTrackingModelFormMixin

from ..models import SubjectVisit


class SubjectModelFormMixin(FormValidatorMixin,
                            VisitTrackingModelFormMixin,
                            JSONModelFormMixin, forms.ModelForm):

    visit_model = SubjectVisit
    visit_attr = 'subject_visit'
