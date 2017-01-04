from django.test import TestCase

from edc_base.utils import get_utcnow

from ..forms import ResidencyMobilityForm

from .test_mixins import SubjectMixin

from edc_constants.constants import YES, NO


class TestResidencyMobilityForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')

        self.options = {
           'permanent_resident': NO,
           'nights_away': 'more than 6 months',
           'subject_visit': self.subject_visit.id,
           'report_datetime': get_utcnow(),
           'length_residence':'6 months to 12 months',
           'intend_residency': YES,
           'cattle_postlands': 'Farm/lands',
           'cattle_postlands_other': 'Not Applicable',
       }
   
      
    def test_form_is_valid(self):
        form = ResidencyMobilityForm(data=self.options)
        self.assertTrue(form.is_valid())
       
    def test_perm_residency_nights_away(self):
        """A permanent resident nights away can\'t be more than 6months otherwise Throw Validation Error"""
        self.options.update(permanent_resident=YES, nights_away='more than 6 months' )
        form = ResidencyMobilityForm(data=self.options)
        self.assertFalse(form.is_valid())
        
        self.options.update(permanent_resident=YES,nights_away='1-6 nights' )
        form = ResidencyMobilityForm(data=self.options)
        self.assertTrue(form.is_valid())
        
    def test_other_community_when_listed(self):
        """If participant was staying in another community, must specify the community, else Throw Validation Error """
        self.options.update(cattle_postlands='Other community', cattle_postlands_other = None)
        form = ResidencyMobilityForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(cattle_postlands='Other community', cattle_postlands_other='Wet lands')
        form = ResidencyMobilityForm(data=self.options)
        self.assertTrue(form.is_valid())
    
    def test_zero_nights_away_and_cattle_postlands(self):
        """A participant with zero nights away times spent away should be Not applicable, else Throw Validation Error """
        self.options.update(nights_away='zero', cattle_postlands = 'Farm/lands')
        form = ResidencyMobilityForm(data=self.options)
        self.assertFalse(form.is_valid()) 

    def test_more_nights_away_and_cattle_postlands(self):
        """Participant has spent more than zero nights away, times spent away CANNOT be Not applicable, else Throw Validation Error"""
        self.options.update(nights_away='6 months to 12 months', cattle_postlands = 'Farm/lands')
        form = ResidencyMobilityForm(data=self.options)
        self.assertFalse(form.is_valid())
        
        
         
