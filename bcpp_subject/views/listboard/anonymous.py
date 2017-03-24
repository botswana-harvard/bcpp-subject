from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ...models import AnonymousConsent
from ..wrappers import AnonymousConsentModelWrapper
from .base_listboard import BaseListboardView


class AnonymousListboardView(BaseListboardView):

    model = AnonymousConsent
    model_wrapper_class = AnonymousConsentModelWrapper
    listboard_url_name = django_apps.get_app_config(
        'bcpp_subject').anonymous_listboard_url_name
    paginate_by = 10
    navbar_name = 'anonymous'
    navbar_item_selected = 'bcpp_subject'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
