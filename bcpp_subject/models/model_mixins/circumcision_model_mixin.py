from django.db import models

from edc_constants.choices import YES_NO_UNSURE

from ..list_models import CircumcisionBenefits


class CircumcisionModelMixin(models.Model):

    circumcised = models.CharField(
        verbose_name="Do you believe that male circumcision"
                     " has any health benefits for you?",
        max_length=15,
        choices=YES_NO_UNSURE,
        null=True,
        help_text="")

    health_benefits_smc = models.ManyToManyField(
        CircumcisionBenefits,
        verbose_name="What do you believe are the health"
                     " benefits of male circumcision? (Indicate all that apply.)",
        blank=True,
        help_text="")

    class Meta:
        abstract = True
