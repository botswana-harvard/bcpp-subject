from edc_search.model_mixins import SearchSlugModelMixin as BaseMixin


class SearchSlugModelMixin(BaseMixin):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        if 'subject_identifier' not in fields:
            fields.append('subject_identifier')
        return fields

    class Meta:
        abstract = True
