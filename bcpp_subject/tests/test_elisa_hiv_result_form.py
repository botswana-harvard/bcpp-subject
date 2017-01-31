from model_mommy import mommy

from django.test import TestCase

from edc_constants.constants import POS, NEG

from ..forms import ElisaHivResultForm
from .test_mixins import SubjectMixin


class TestElisaHivResultForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()

        mommy.make_recipe(
            'bcpp_subject.subjectrequisition',
            subject_visit=self.subject_visit_female,
            report_datetime=self.get_utcnow(),
            panel_name='ELISA',
        )

        self.options = {
            'report_datetime': self.get_utcnow(),
            'subject_visit': self.subject_visit_female.id,
            'hiv_result': NEG,
            'hiv_result_datetime': self.get_utcnow(),
        }

    def test_form_is_valid(self):
        elisa_hiv_result_form = ElisaHivResultForm(data=self.options)
        self.assertTrue(elisa_hiv_result_form.is_valid())
        self.assertTrue(elisa_hiv_result_form.save())

    def test_no_date_time(self):
        """Assert test with negative results was carried out
        without date provided.
        """
        self.options.update(hiv_result_datetime=None)
        elisa_hiv_result_form = ElisaHivResultForm(data=self.options)
        self.assertFalse(elisa_hiv_result_form.is_valid())

    def test_no_date_time_for_pos(self):
        """Assert test with positive results was carried out
        without date provided.
        """
        self.options.update(hiv_result=POS, hiv_result_datetime=None)
        elisa_hiv_result_form = ElisaHivResultForm(data=self.options)
        self.assertFalse(elisa_hiv_result_form.is_valid())
