from django.views.generic import TemplateView, FormView

from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import MALE
from edc_dashboard.view_mixins import ListboardViewMixin, AppConfigViewMixin

from survey import SurveyViewMixin


class ListboardView(ListboardViewMixin, SurveyViewMixin,
                    AppConfigViewMixin, EdcBaseViewMixin,
                    TemplateView, FormView):

    app_config_name = 'bcpp_subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            MALE=MALE,
            reference_datetime=get_utcnow(),
        )
        context.update(
            {k: v for k, v in self.url_names('anonymous_listboard_url_name')})
        return context
