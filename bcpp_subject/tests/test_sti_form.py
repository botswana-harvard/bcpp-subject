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
            'yeast_infection_date': date(2016, 9, 7),
            'pneumonia_date': date(2016, 12, 7),
            'pcp_date': date(2016, 12, 12),
            'herpes_date': datetime.today(),
            'comments': 'diagnosed',
            'subject_visit': self.subject_visit.id,
            'report_datetime': get_utcnow(),
        }

    def test_valid_form(self):
        form = StiForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_if_sti_dx_detected_wasting(self):
        """Testing if severe weight loss (wasting) - more than 10% of body weight"""
        self.still_illnesses.name = 'Severe weight loss (wasting) - more than 10% of body weight'
        self.still_illnesses.save()
        self.options.update(wasting_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_sti_dx_detected_diarrhoea(self):
        """Testing to see if diarrhoea was detected during diagnosis"""
        self.still_illnesses.name = 'Unexplained diarrhoea for one month'
        self.still_illnesses.save()
        self.options.update(diarrhoea_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_sti_dx_detected_yeast_infection(self):
        """Testing to see if yeast was detected during diagnosis"""
        self.still_illnesses.name = 'Yeast infection of mouth or oesophagus'
        self.still_illnesses.save()
        self.options.update(yeast_infection_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_sti_dx_detected_pneumonia_infection(self):
        """Testing to see if severe pneumonia or meningitis or sepsis during diagnosis"""
        self.still_illnesses.name = 'Severe pneumonia or meningitis or sepsis'
        self.still_illnesses.save()
        self.options.update(pneumonia_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_sti_dx_detected_pcp_infection(self):
        """Testing to see if PCP during diagnosis"""
        self.still_illnesses.name = 'PCP (Pneumocystis pneumonia)'
        self.still_illnesses.save()
        self.options.update(pcp_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_sti_dx_detected_herpes_infection(self):
        """Testing to see if Herpes infection for more than one month detected during diagnosis"""
        self.still_illnesses.name = 'Herpes infection for more than one month'
        self.still_illnesses.save()
        self.options.update(herpes_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())
