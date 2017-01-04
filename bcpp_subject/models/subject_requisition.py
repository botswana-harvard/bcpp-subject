from edc_lab.model_mixins import RequisitionModelMixin

from .model_mixins import CrfModelMixinNonUniqueVisit


class SubjectRequisition(RequisitionModelMixin, CrfModelMixinNonUniqueVisit):

    class Meta(CrfModelMixinNonUniqueVisit.Meta):
        app_label = 'bcpp_subject'
