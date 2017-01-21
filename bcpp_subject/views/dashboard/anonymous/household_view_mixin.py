from plot.utils import get_anonymous_plot

from household.views import HouseholdViewMixin as BaseHouseholdViewMixin


class HouseholdViewMixin(BaseHouseholdViewMixin):

    def get(self, request, *args, **kwargs):
        plot = get_anonymous_plot()
        household = plot.household_set.all().last()
        try:
            kwargs['household_identifier'] = household.household_identifier
        except AttributeError:
            kwargs['household_identifier'] = None
        return super().get(request, *args, **kwargs)
