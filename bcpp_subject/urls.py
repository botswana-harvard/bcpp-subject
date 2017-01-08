from django.conf.urls import url

from edc_constants.constants import UUID_PATTERN

from survey.patterns import survey

from .admin_site import bcpp_subject_admin
from .patterns import subject_identifier
from .views import ListView, DashboardView

urlpatterns = [
    url(r'^admin/', bcpp_subject_admin.urls),
    url(r'^list/(?P<page>\d+)/', ListView.as_view(), name='list_url'),
    url(r'^list/', ListView.as_view(), name='list_url'),
    url(r'^dashboard/(?P<subject_identifier>' + subject_identifier + ')/(?P<appointment>[0-9a-f-]+)/(?P<survey>' + survey + ')/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/(?P<subject_identifier>' + subject_identifier + ')/(?P<survey>' + survey + ')/(?P<page>\d+)/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/(?P<subject_identifier>' + subject_identifier + ')/(?P<survey>' + survey + ')/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/(?P<subject_identifier>' + UUID_PATTERN.pattern + ')/(?P<survey>' + survey + ')/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/(?P<subject_identifier>' + subject_identifier + ')/',
        DashboardView.as_view(), name='dashboard_url'),
]
