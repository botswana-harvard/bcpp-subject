from model_mommy import mommy

from edc_base_test.mixins import LoadListDataMixin

from member.list_data import list_data
from member.tests.test_mixins import MemberMixin


class SubjectTestMixin(MemberMixin, LoadListDataMixin):

    list_data = list_data


class SubjectMixin(SubjectTestMixin):

    def setUp(self):
        super(SubjectMixin, self).setUp()
        self.study_site = '40'
