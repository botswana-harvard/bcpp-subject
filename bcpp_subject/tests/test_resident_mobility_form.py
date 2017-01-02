from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..forms import ResidencyMobilityForm
from .test_mixins import SubjectMixin


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
   
   # @author: MAGODI GOFAONE
   #  DATE: 30 DEC 2016     
   def test_form_is_valid(self):
       form = ResidencyMobilityForm(data=self.options)
       self.assertTrue(form.is_valid())
       
   # @author: MAGODI GOFAONE
   #  DATE: 30 DEC 2016
   def test_perm_residency_nights_away_more_six_months(self):
       """Test participant is a permanent with more than six months away"""
       self.options.update(permanent_resident=YES, nights_away ='more than 6 months')
       form = ResidencyMobilityForm(data=self.options)
       self.assertFalse(form.is_valid())
    
   # @author: MAGODI GOFAONE
   #  DATE: 30 DEC 2016
   def test_state_other_community_listed(self):
       """Test participant was staying in another community, specify the community"""
       self.options.update(cattle_postlands='Other community', cattle_postlands_other = None)
       form = ResidencyMobilityForm(data=self.options)
       self.assertFalse(form.is_valid())
#         self.assertRaises(ValidationError, form.save)

   # @author: MAGODI GOFAONE
   #  DATE: 30 DEC 2016     
   def test_zero_nights_away_not_na_cattle_postlands(self):
       """Test participant with zero nights away and has a cattle post lands specified"""
       self.options.update(nights_away='zero', cattle_postlands = 'Farm/lands')
       form = ResidencyMobilityForm(data=self.options)
       self.assertFalse(form.is_valid())
       
   # @author: MAGODI GOFAONE
   #  DATE: 30 DEC 2016  
   def test_nights_away_not_zero_cattle_postlands_is_na(self):
       """Test participant with more than zero nights away and has no cattle post lands specified"""
       self.options.update(cattle_postlands = 'Not Applicable', nights_away='more than 6 months')
       form = ResidencyMobilityForm(data=self.options)
       self.assertFalse(form.is_valid())