from django import forms

from edc_constants.constants import NOT_APPLICABLE, NEG, POS, IND, YES, NO

from ..models import HivResult, SubjectRequisition, HicEnrollment

from .form_mixins import SubjectModelFormMixin


class HivResultForm (SubjectModelFormMixin):

    def clean(self):

        cleaned_data = super(HivResultForm, self).clean()

        try:
            HicEnrollment.objects.get(subject_visit=cleaned_data.get('subject_visit'))
        except HicEnrollment.DoesNotExist:
            pass
        else:
            if cleaned_data.get('hiv_result') != NEG:
                raise forms.ValidationError(
                    'Result cannot be changed. {} exists for this subject. '
                    'Got {0}'.format(HicEnrollment._meta.verbose_name,
                                     cleaned_data.get('hiv_result')))
        try:
            SubjectRequisition.objects.get(
                subject_visit=cleaned_data.get('subject_visit'),
                panel_name='Microtube')
        except SubjectRequisition.DoesNotExist:
            raise forms.ValidationError(
                'Please complete Microtube Requisition first.')

        # validating when testing declined
        if cleaned_data.get('hiv_result') == 'Declined' and not cleaned_data.get('why_not_tested'):
            raise forms.ValidationError(
                'If participant has declined testing, provide reason participant declined testing')

        # validating when testing not performed
        if cleaned_data.get('hiv_result') == 'Not performed' and cleaned_data.get('why_not_tested'):
            raise forms.ValidationError(
                {'why_not_tested': 'This field is not required.'})

        # testing declined but giving test date
        result_declined = (cleaned_data.get('hiv_result') == 'Declined')
        result_not_performed = (cleaned_data.get('hiv_result') == 'Not performed')
        if (result_declined or result_not_performed) and (cleaned_data.get('hiv_result_datetime')):
            raise forms.ValidationError(
                {'hiv_result_datetime': 'This field is not required.'})

        # testing done but giving reason why not done
        if(
           (cleaned_data.get('hiv_result') == POS) or
           (cleaned_data.get('hiv_result') == NEG) or
           (cleaned_data.get('hiv_result') == IND)) and (cleaned_data.get('why_not_tested')):
            raise forms.ValidationError(
                {'why_not_tested': 'This field is not required.'})

        # testing done but not providing date
        if(
           (cleaned_data.get('hiv_result') == POS) or
           (cleaned_data.get('hiv_result') == NEG) or
           (cleaned_data.get('hiv_result') == IND)) and not (cleaned_data.get('hiv_result_datetime')):
            raise forms.ValidationError(
                {'hiv_result_datetime': 'This field is required.'})
        self.validate_hiv_status_nd_blood_draw_type()
        if(
           cleaned_data.get('hiv_result') not in [POS, NEG, IND] and
           cleaned_data.get('insufficient_vol') in [YES, NO]):
            raise forms.ValidationError(
                'No blood drawn.  You do not need to indicate if volume '
                'is sufficient. Got {0}'.format(cleaned_data.get('insufficient_vol')))
        if(
           cleaned_data.get('hiv_result') in [POS, NEG, IND] and
           cleaned_data.get('blood_draw_type') not in ['capillary', 'venous']):
            raise forms.ValidationError('Blood was drawn. Please indicate the type.')
        return cleaned_data

    def validate_hiv_status_nd_blood_draw_type(self):
        cleaned_data = self.cleaned_data
        if(
           cleaned_data.get('hiv_result') not in [POS, NEG, IND] and
           cleaned_data.get('blood_draw_type') in ['capillary', 'venous']):
            raise forms.ValidationError(
                'No blood drawn but you said {0}. Please correct.'.format(
                    cleaned_data.get('blood_draw_type')))
        if(
           cleaned_data.get('blood_draw_type') == 'capillary' and
           cleaned_data.get('insufficient_vol') == NOT_APPLICABLE):
            raise forms.ValidationError('Please indicate if the capillary tube has sufficient volume.')
        if cleaned_data.get('blood_draw_type') == 'venous' and cleaned_data.get('insufficient_vol') in [YES, NO]:
            raise forms.ValidationError(
                'Venous blood drawn.  You do not need to indicate if volume is '
                'sufficient. Got {0}'.format(cleaned_data.get('insufficient_vol')))

    class Meta:
        model = HivResult
        fields = '__all__'
