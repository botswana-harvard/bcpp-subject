from django.contrib.admin import AdminSite


class BcppSubjectAdminSite(AdminSite):
    site_title = 'BCPP Subject'
    site_header = 'BCPP Subject'
    index_title = 'BCPP Subject'
    site_url = '/bcpp_subject/list/'
bcpp_subject_admin = BcppSubjectAdminSite(name='bcpp_subject_admin')


class BcppSubjectAHST2AdminSite(AdminSite):
    site_title = 'BCPP Subject AHS T2'
    site_header = 'BCPP Subject AHS T2'
    index_title = 'BCPP Subject AHS T2'
    site_url = '/bcpp_subject/list/'
bcpp_subject_ahs_t2_admin = BcppSubjectAHST2AdminSite(name='bcpp_subject_ahs_t2_admin')
