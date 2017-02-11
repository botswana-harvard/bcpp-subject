from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import MALE
from edc_dashboard.view_mixins import AppConfigViewMixin
from edc_dashboard.views import ListboardView

from survey import SurveyViewMixin


class BaseListboardView(SurveyViewMixin, AppConfigViewMixin, EdcBaseViewMixin,
                        ListboardView):

    app_config_name = 'bcpp_subject'
    navbar_item_selected = 'bcpp_subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            MALE=MALE,
            reference_datetime=get_utcnow())
        context.update(
            {k: v for k, v in self.url_names('anonymous_listboard_url_name')})
        return context
