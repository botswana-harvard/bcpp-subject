from django.conf.urls import url

from .admin_site import bcpp_subject_admin

# app_name = 'bcpp_subject'

urlpatterns = [url(r'^admin/', bcpp_subject_admin.urls)]
