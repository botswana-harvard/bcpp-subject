from django import forms

from edc_constants.constants import (
    NOT_APPLICABLE, NEG, POS, IND, YES, NO, DECLINED)

from ..models import HivResult, SubjectRequisition, HicEnrollment

from .form_mixins import SubjectModelFormMixin
from bcpp_subject.constants import NOT_PERFORMED, CAPILLARY, VENOUS


class HivResultForm (SubjectModelFormMixin):

    def clean(self):

        cleaned_data = super().clean()

        try:
            HicEnrollment.objects.get(
                subject_visit=cleaned_data.get('subject_visit'))
        except HicEnrollment.DoesNotExist:
            pass
        else:
            if cleaned_data.get('hiv_result') != NEG:
                raise forms.ValidationError(
                    'Result cannot be changed. {} exists for this subject. '
                    'Got {0}'.format(HicEnrollment._meta.verbose_name,
                                     cleaned_data.get('hiv_result')))

#         try:
#             microtube = SubjectRequisition.objects.get(
#                 subject_visit=cleaned_data.get('subject_visit'),
#                 panel_name='Microtube')
#         except SubjectRequisition.DoesNotExist:
#             microtube = None
#
#         if (cleaned_data.get('hiv_result') not in [DECLINED, NOT_PERFORMED]
#                 and not microtube):
#             raise forms.ValidationError(
#                 'Please complete Microtube Requisition first.')

        self.required_if(
            POS, NEG, IND, field='hiv_result', field_required='hiv_result_datetime')

        self.applicable_if(
            POS, NEG, IND, field='hiv_result', field_applicable='blood_draw_type')
        self.applicable_if(
            CAPILLARY, VENOUS, field='blood_draw_type', field_applicable='insufficient_vol')

        self.required_if(
            DECLINED, NOT_PERFORMED, field='hiv_result', field_required='why_not_tested')

        return cleaned_data

    class Meta:
        model = HivResult
        fields = '__all__'
