from edc_base.model.models import ListModelMixin, BaseUuidModel


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


class EthnicGroups (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Ethnic groups"


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


class MedicalCareAccess (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Medical care access"


class MedicationTaken (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Medical taken"


class HospitalizationReason (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Hospitalization Reasons"


class ChronicDisease (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Chronic Diseases"


class MedicationGiven(ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Medical given"


class NeighbourhoodProblems (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Neighbourhood problems"


class PartnerResidency (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Partner residency"


class Religion (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "Religion"


class ResidentMostLikely (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name_plural = "Resident most likely"


class StiIllnesses (ListModelMixin, BaseUuidModel):

    class Meta(ListModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "HIV-related illness"
        verbose_name_plural = "HIV-related illnesses"
