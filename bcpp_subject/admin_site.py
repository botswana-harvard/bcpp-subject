from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = 'BCPP Subject'
    site_header = 'BCPP Subject'
    index_title = 'BCPP Subject'
    site_url = '/bcpp_subject/list/'


bcpp_subject_admin = AdminSite(name='bcpp_subject_admin')
