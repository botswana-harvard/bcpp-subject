from django.test import TestCase

from edc_constants.constants import OTHER

from ..constants import ZAMBIA, NO_PERMIT, NARNIA
from ..forms import ImmigrationStatusForm
from .test_mixins import SubjectMixin


class TestImmigrationStatus(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()

        self.data = {
            'country_of_origin': ZAMBIA,
            'country_of_origin_other': None,
            'immigration_status': NO_PERMIT,
            'subject_visit': self.subject_visit_male.id,
            'report_datetime': self.get_utcnow()}

    def test_valid_form(self):
        form = ImmigrationStatusForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_other_country_validation(self):
        self.data.update(
            country_of_origin_other=NARNIA)
        form = ImmigrationStatusForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_country_validation(self):
        self.data.update(
            country_of_origin=OTHER)
        form = ImmigrationStatusForm(data=self.data)
        self.assertFalse(form.is_valid())
