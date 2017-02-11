from edc_dashboard.model_mixins import SearchSlugModelMixin as BaseSearchSlugModelMixin


class SearchSlugModelMixin(BaseSearchSlugModelMixin):

    def get_slugs(self):
        slugs = super().get_slugs()
        return slugs + [
            self.subject_identifier] + self.household_member.get_slugs()

    class Meta:
        abstract = True
