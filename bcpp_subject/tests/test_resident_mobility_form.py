from django.test import TestCase

from ..forms import ResidencyMobilityForm

from .test_mixins import SubjectMixin

from edc_constants.constants import YES, NO


class TestResidencyMobilityForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.consent_data = {
            'identity': '31721515',
            'confirm_identity': '31721515',
            'report_datetime': self.get_utcnow(),
        }
        self.bhs_subject_visit_male = self.make_subject_visit_for_consented_subject_male('T0', **self.consent_data)

        self.options = {
            'permanent_resident': NO,
            'nights_away': 'more than 6 months',
            'subject_visit': self.bhs_subject_visit_male.id,
            'report_datetime': self.get_utcnow(),
            'length_residence': '6 months to 12 months',
            'intend_residency': YES,
            'cattle_postlands': 'Farm/lands',
            'cattle_postlands_other': 'Not Applicable', }

    def test_form_is_valid(self):
        form = ResidencyMobilityForm(data=self.options)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_perm_residency_nights_away(self):
        """Assert permanent resident cannot be more than 6months away
                otherwise raise Validation Error. """
        self.options.update(permanent_resident=YES,
                            nights_away='more than 6 months')
        form = ResidencyMobilityForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(permanent_resident=YES, nights_away='1-6 nights')
        form = ResidencyMobilityForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_other_community_when_listed(self):
        """ Assert participant staying in another community, must specify the
         community, else raise Validation Error. """
        self.options.update(cattle_postlands='Other community',
                            cattle_postlands_other=None)
        form = ResidencyMobilityForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(cattle_postlands='Other community',
                            cattle_postlands_other='Wet lands')
        form = ResidencyMobilityForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_zero_nights_away_and_cattle_postlands(self):
        """ Assert participant with zero nights away times spent away
        should be Not applicable, else raise Validation Error. """
        self.options.update(nights_away='zero', cattle_postlands='Farm/lands')
        form = ResidencyMobilityForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_more_nights_away_and_cattle_postlands(self):
        """ Assert participant with nights away, times spent away
         cannot be Not applicable, else raise Validation Error. """
        self.options.update(nights_away='6 months to 12 months',
                            cattle_postlands='Farm/lands')
        form = ResidencyMobilityForm(data=self.options)
        self.assertFalse(form.is_valid())
