from django.db import models

from .model_mixins import CrfModelMixin

from ..choices import COUNTRIES


# FIXME
# added the countries to the choices
# COUNTRIES = (('country', 'Country'), )

IMMIGRATION_STATUS = (
    ('visitor_permit', 'In Botswana with visitor’s permit'),
    ('residency_permit', 'In Botswana with residency permit'),
    ('no_permit', 'In Botswana without permit')
)


class ImmigrationStatus(CrfModelMixin):

    country_of_origin = models.CharField(
        verbose_name='What is your country of origin?',
        max_length=25,
        choices=COUNTRIES
    )

    country_of_origin_other = models.CharField(
        verbose_name='If other was selected, above, write down your country '
        'of origin?',
        max_length=50,
        null=True,
        blank=True)

    immigration_status = models.CharField(
        verbose_name='What is your immigration status in Botswana?',
        max_length=25,
        choices=IMMIGRATION_STATUS)

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Immigration Status"
        verbose_name_plural = "Immigration Status"
