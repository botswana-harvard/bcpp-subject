from django.conf.urls import url
from django.contrib import admin
from .admin_site import bcpp_subject_admin

urlpatterns = [
#     url(r'^admin/', admin.site.urls),
    url(r'^admin/', bcpp_subject_admin.urls),
]
