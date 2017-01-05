from django.test import TestCase

from ..forms import SexualBehaviourForm

from .test_mixins import SubjectMixin

from edc_constants.constants import YES, NO


class TestSexualBehaviourForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject(
            'T0')

        self.options = {
           'subject_visit': self.subject_visit.id,
           'report_datetime': self.get_utcnow(),
           'ever_sex': YES,
           'lifetime_sex_partners':  3,
           'more_sex': YES,
           'last_year_partners': 1,
           'condom': YES,
           'alcohol_sex': 'Myself', }

    def test_form_is_valid(self):
        form = SexualBehaviourForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_had_sex_and_lifetime_sex_partners(self):
        """ Assert participant has never had sex, cannot have none lifetime partners
            ,otherwise raise validation error. """
        self.options.update(ever_sex=YES, lifetime_sex_partners=None)
        form = SexualBehaviourForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(ever_sex=YES, lifetime_sex_partners=3)
        form = SexualBehaviourForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_more_sex_last_year_sex_partners(self):
        """ Assert participant has never had sex with somebody living outside of the '
            'community, cannot have 0 last year partners, else
                raise validation error."""
        self.options.update(last_year_partners=None)
        form = SexualBehaviourForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(last_year_partners=3)
        form = SexualBehaviourForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_has_last_year_partners_none_more_sex(self):
        """ Assert participant has had sex with anyone in the past 12months,specify if
            participant had sex with anyone outside community in the past
            12months otherwise throw validation error."""
        self.options.update(more_sex=None)
        form = SexualBehaviourForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(more_sex=YES)
        form = SexualBehaviourForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_had_sex_none_condom(self):
        """ Assert participant has had sex at some point in their life, specify if
            participant used a Condom the last time he/she had sex,otherwise
                throw validation error."""
        self.options.update(condom=None)
        form = SexualBehaviourForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(condom=YES)
        form = SexualBehaviourForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_had_sex_none_alcohol_sex(self):
        """ Assert participant has had sex at some point in their life, specify if
            participant drank alcohol before sex last time, otherwise throw
                validation error."""
        self.options.update(alcohol_sex=None)
        form = SexualBehaviourForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(alcohol_sex='My partner')
        form = SexualBehaviourForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_compare_last_year_sex_partners_with_lifetime_sex_partners(self):
        """ Assert Number of partners in the past 12months exceed number of life
        time partners,throw validation error. """
        self.options.update(lifetime_sex_partners=4, last_year_partners=9)
        form = SexualBehaviourForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_validate_dependent_fields(self):
        """Assert participant never had sex,no sex related follow-up
            questions asked"""
        self.options.update(ever_sex=NO)
        form = SexualBehaviourForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(ever_sex=NO, lifetime_sex_partners=0,
                            last_year_partners=0, more_sex=None,
                            first_sex=None, condom=None, alcohol_sex=None)
        form = SexualBehaviourForm(data=self.options)
        self.assertTrue(form.is_valid())
