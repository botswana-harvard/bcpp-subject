from django.conf.urls import url

from edc_constants.constants import UUID_PATTERN

from survey.patterns import survey, survey_schedule

from .admin_site import bcpp_subject_admin
from .patterns import subject_identifier
from .views import ListBoardView, DashboardView

urlpatterns = [
    url(r'^admin/', bcpp_subject_admin.urls),
    url(r'^listboard/'
        '(?P<subject_identifier>' + subject_identifier + ')/'
        '(?P<survey_schedule>' + survey_schedule + ')/'
        '(?P<page>\d+)/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^listboard/'
        '(?P<subject_identifier>' + subject_identifier + ')/'
        '(?P<survey>' + survey + ')/'
        '(?P<page>\d+)/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^listboard/(?P<subject_identifier>' + subject_identifier + ')/'
        '(?P<survey_schedule>' + survey_schedule + ')/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^listboard/'
        '(?P<subject_identifier>' + subject_identifier + ')/'
        '(?P<survey>' + survey + ')/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^listboard/(?P<subject_identifier>' + subject_identifier + ')/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^listboard/(?P<page>\d+)/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^listboard/',
        ListBoardView.as_view(), name='listboard_url'),
    url(r'^dashboard/'
        '(?P<subject_identifier>' + subject_identifier + ')/'
        '(?P<appointment>[0-9a-f-]+)/'
        '(?P<survey>' + survey + ')/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/'
        '(?P<subject_identifier>' + subject_identifier + ')/'
        '(?P<survey_schedule>' + survey_schedule + ')/'
        '(?P<page>\d+)/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/'
        '(?P<subject_identifier>' + subject_identifier + ')/'
        '(?P<survey>' + survey + ')/'
        '(?P<page>\d+)/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/'
        '(?P<subject_identifier>' + subject_identifier + ')/'
        '(?P<survey_schedule>' + survey_schedule + ')/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/'
        '(?P<subject_identifier>' + subject_identifier + ')/'
        '(?P<survey>' + survey + ')/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/'
        '(?P<subject_identifier>' + UUID_PATTERN.pattern + ')/'
        '(?P<survey_schedule>' + survey_schedule + ')/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/'
        '(?P<subject_identifier>' + UUID_PATTERN.pattern + ')/'
        '(?P<survey>' + survey + ')/',
        DashboardView.as_view(), name='dashboard_url'),
    url(r'^dashboard/(?P<subject_identifier>' + subject_identifier + ')/',
        DashboardView.as_view(), name='dashboard_url'),
]
