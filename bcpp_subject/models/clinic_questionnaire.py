from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_DWTA, YES_NO
from edc_constants.constants import YES, POS, NO

from ..choices import VERBAL_HIVRESULT_CHOICE
from ..exceptions import ClinicQuestionnaireError

from .model_mixins import CrfModelMixin, CrfModelManager


class ClinicQuestionnaire (CrfModelMixin):

    know_hiv_status = models.CharField(
        verbose_name="Do you know your current HIV status?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="")

    current_hiv_status = models.CharField(
        verbose_name="Please tell me your current HIV status?",
        max_length=30,
        null=True,
        blank=True,
        choices=VERBAL_HIVRESULT_CHOICE,
        help_text="")

    on_arv = models.CharField(
        verbose_name="Are you currently taking antiretroviral therapy (ARVs)?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="")

    arv_evidence = models.CharField(
        verbose_name="Is there evidence [OPD card, tablets, masa number] that the participant is on therapy?",
        choices=YES_NO,
        null=True,
        blank=True,
        max_length=3)

    objects = CrfModelManager()

    history = HistoricalRecords()

    def common_clean(self):
        # if knowing HIV status
        if self.know_hiv_status == YES and not self.current_hiv_status:
            raise ClinicQuestionnaireError(
                'If participant knows their HIV status, ask the participant to tell you the current HIV status', 'know_hiv_status')
        # if POS, on ARV?
        if self.current_hiv_status == POS and not self.on_arv:
            raise ClinicQuestionnaireError('If participant is HIV positive, is participant on ARV therapy?', 'current_hiv_status')
        # if on ARV, is there evidence
        if self.on_arv == YES and not self.arv_evidence:
            raise ClinicQuestionnaireError(
                'If participant is on ARV, is there evidence of being on therapy [OPD card, tablets, masa number]?', 'on_arv')
        # NO
        if (self.know_hiv_status == NO and (self.current_hiv_status or self.on_arv or self.arv_evidence)):
            raise ClinicQuestionnaireError(
                'If participant does not know their HIV status, do not provide any other details', 'know_hiv_status')

    @property
    def common_clean_exceptions(self):
        common_clean_exceptions = super().common_clean_exceptions
        common_clean_exceptions.extend([ClinicQuestionnaireError])
        return common_clean_exceptions

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Clinic Questionnaire"
        verbose_name_plural = "Clinic Questionnaire"
