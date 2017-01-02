from datetime import datetime, date

from django.test import TestCase
from django.utils import timezone

from edc_base.utils import get_utcnow

from ..forms import StiForm

from .test_mixins import SubjectMixin

from ..models.list_models import StiIllnesses


class TestStiForm(SubjectMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')
        self.still_illnesses = StiIllnesses.objects.create(
            name='Unexplained diarrhoea for one month', short_name='Unexplained diarrhoea for one month')

        self.options = {
            'sti_dx': [str(self.still_illnesses.id)],
            'sti_dx_other': None,
            'wasting_date': date(2016, 11, 10),
            'diarrhoea_date': date(2016, 7, 7),
            'yeast_infection_date': date(2016, 7, 7),
            'pneumonia_date': date(2016, 12, 7),
            'pcp_date': timezone.now(),
            'herpes_date': datetime.today(),
            'comments': 'diagnosed',
            'subject_visit': self.subject_visit.id,
            'report_datetime': get_utcnow(),
        }

    def test_valid_form(self):
        """Test to verify whether form will submit"""
        form = StiForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_if_sti_dx_detected_wasting(self):
        """Testing if severe weight loss (wasting) - more than 10% of body weight"""
        self.still_illnesses.name = 'HIV dementia'
        self.options.update(sti_dx=[str(self.still_illnesses.id)])
        form = StiForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_if_sti_dx_not_detected_wasting(self):
        """Testing if severe weight loss (wasting) -  not more than 10% of body weight"""
        self.still_illnesses.name = 'pcc'
        self.options.update(sti_dx=[str(self.still_illnesses.id)])
        form = StiForm(data=self.options)
        self.assertTrue(form.is_valid())
