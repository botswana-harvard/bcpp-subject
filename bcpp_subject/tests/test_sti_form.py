from django.test import TestCase

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
            'wasting_date': self.get_utcnow().date(),
            'diarrhoea_date': self.get_utcnow().date(),
            'yeast_infection_date': self.get_utcnow().date(),
            'pneumonia_date': self.get_utcnow().date(),
            'pcp_date': self.get_utcnow().date(),
            'herpes_date': self.get_utcnow().date(),
            'comments': 'diagnosed',
            'subject_visit': self.subject_visit.id,
            'report_datetime': self.get_utcnow(),
        }

    def test_valid_form(self):
        form = StiForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_if_sti_dx_detected_wasting(self):
        """Asserts that severe weight loss (wasting) - more than 10% of body weight"""
        self.still_illnesses.name = 'Severe weight loss (wasting) - more than 10% of body weight'
        self.still_illnesses.save()
        self.options.update(wasting_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_sti_dx_detected_diarrhoea(self):
        """Asserts that diarrhoea was detected during diagnosis"""
        self.still_illnesses.name = 'Unexplained diarrhoea for one month'
        self.still_illnesses.save()
        self.options.update(diarrhoea_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_sti_dx_detected_yeast_infection(self):
        """Asserts that yeast was detected during diagnosis"""
        self.still_illnesses.name = 'Yeast infection of mouth or oesophagus'
        self.still_illnesses.save()
        self.options.update(yeast_infection_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_sti_dx_detected_pneumonia_infection(self):
        """Asserts that severe pneumonia or meningitis or sepsis during diagnosis"""
        self.still_illnesses.name = 'Severe pneumonia or meningitis or sepsis'
        self.still_illnesses.save()
        self.options.update(pneumonia_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_sti_dx_detected_pcp_infection(self):
        """Assert that PCP during diagnosis"""
        self.still_illnesses.name = 'PCP (Pneumocystis pneumonia)'
        self.still_illnesses.save()
        self.options.update(pcp_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_sti_dx_detected_herpes_infection(self):
        """Asserts that Herpes infection for more than one month detected during diagnosis"""
        self.still_illnesses.name = 'Herpes infection for more than one month'
        self.still_illnesses.save()
        self.options.update(herpes_date=None)
        form = StiForm(data=self.options)
        self.assertFalse(form.is_valid())
