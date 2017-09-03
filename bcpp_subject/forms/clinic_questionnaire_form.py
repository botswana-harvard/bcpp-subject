from ..models import ClinicQuestionnaire
from .form_mixins import SubjectModelFormMixin


class ClinicQuestionnaireForm (SubjectModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = ClinicQuestionnaire
        fields = '__all__'


"""
        # if knowing HIV status
        if self.know_hiv_status == YES and not self.current_hiv_status:
            raise ClinicQuestionnaireError(
                "If participant knows their HIV status, ask the participant "
                "to tell you the current HIV status', 'know_hiv_status")
        # if POS, on ARV?
        if self.current_hiv_status == POS and not self.on_arv:
            raise ClinicQuestionnaireError(
                "If participant is HIV positive, "
                "is participant on ARV therapy?', 'current_hiv_status")
        # if on ARV, is there evidence
        if self.on_arv == YES and not self.arv_evidence:
            raise ClinicQuestionnaireError(
                "If participant is on ARV, is there evidence of being on "
                "therapy [OPD card, tablets, masa number]?', 'on_arv")
        # NO
        if (self.know_hiv_status == NO and (
                self.current_hiv_status or self.on_arv or self.arv_evidence)):
            raise ClinicQuestionnaireError(
                'If participant does not know their HIV status, '
                'do not provide any other details', 'know_hiv_status')

"""
