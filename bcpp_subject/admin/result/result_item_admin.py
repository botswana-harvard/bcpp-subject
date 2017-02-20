from django.contrib import admin

from edc_lab.admin_site import edc_lab_admin

from ...models import ResultItem
from ..modeladmin_mixins import ModelAdminMixin


@admin.register(ResultItem, site=edc_lab_admin)
class ResultItemAdmin(ModelAdminMixin, admin.ModelAdmin):
    pass


class ResultItemInlineAdmin(ModelAdminMixin, admin.TabularInline):
    model = ResultItem
    extra = 0

    fields = ('utestid', 'value', 'quantifier', 'value_datetime')
