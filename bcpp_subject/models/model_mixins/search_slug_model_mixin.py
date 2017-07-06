from edc_search.model_mixins import SearchSlugModelMixin as BaseMixin


class SearchSlugModelMixin(BaseMixin):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('subject_identifier')
        fields.extend(self.household_member.get_search_slug_fields())
        fields = list(set(fields))
        return fields

    class Meta:
        abstract = True
