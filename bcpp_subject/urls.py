from django.conf.urls import url

from .admin_site import bcpp_subject_admin
from .patterns import subject_identifier
from .views import BcppSubjectsView, DashboardView

urlpatterns = [
    url(r'^admin/', bcpp_subject_admin.urls),
    url(r'^list/(?P<page>\d+)/', BcppSubjectsView.as_view(), name='list_url'),
    url(r'^list/', BcppSubjectsView.as_view(), name='list_url'),
    url(r'^dashboard/(?P<subject_identifier>' + subject_identifier + ')/(?P<selected_appointment>[0-9a-f-]+)/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/(?P<subject_identifier>' + subject_identifier + ')/(?P<page>\d+)/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/(?P<subject_identifier>' + subject_identifier + ')/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/(?P<member>[0-9a-f-]+)/',
        DashboardView.as_view(), name='dashboard_url'),
]
