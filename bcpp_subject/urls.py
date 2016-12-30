from django.conf.urls import url

from .admin_site import bcpp_subject_admin
from .views import BcppSubjectsView

urlpatterns = [
    url(r'^admin/', bcpp_subject_admin.urls),
    url(r'^list/(?P<page>\d+)/', BcppSubjectsView.as_view(), name='list_url'),
    url(r'^list/', BcppSubjectsView.as_view(), name='list_url'),
]
