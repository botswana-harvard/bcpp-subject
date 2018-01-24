from edc_base.model_mixins import ListModelMixin, BaseUuidModel


class Arv (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"


class CircumcisionBenefits (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Circumcision benefits"


class Diagnoses (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "Diagnoses"
        verbose_name_plural = "Diagnoses"


class FamilyPlanning (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Family planning"


class HeartDisease (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Heart disease"


class LiveWith (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Living with"


class TestsOrdered (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Tests Ordered"


class MedicationPrescribed (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Medication Prescribed"


class MedicalCareAccess (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Medical care access"


class Medication (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Medication"


class NeighbourhoodProblems (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Neighbourhood problems"


class PartnerResidency (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Partner residency"


class ResidentMostLikely (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Resident most likely"


class StiIllnesses (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "HIV-related illness"
        verbose_name_plural = "HIV-related illnesses"
