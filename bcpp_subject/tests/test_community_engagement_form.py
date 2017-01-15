from django.test import TestCase

from edc_constants.constants import YES, DWTA

from ..forms import CommunityEngagementForm

from .test_mixins import SubjectMixin

from ..models.list_models import NeighbourhoodProblems

from bcpp_subject.models.list_models import Diagnoses


class TestCommunityEngagementForm(SubjectMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')
        self.diagnoses = Diagnoses.objects.create(name='STI (Sexually Transmitted Infection)', short_name='STI (Sexually Transmitted Infection')
        self.neighboourhood_problems = NeighbourhoodProblems.objects.create(
            name='theft in the neighbourhood', short_name='theft')

        self.options = {
            'community_engagement': 'Very active',
            'vote_engagement': YES,
            'problems_engagement': [str(self.neighboourhood_problems.id)],
            'problems_engagement_other': None,
            'solve_engagement': YES,
            'subject_visit': self.subject_visit.id,
            'report_datetime': self.get_utcnow(),
        }

    def test_valid_form(self):
        form = CommunityEngagementForm(data=self.options)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_community_engagement_reponse_to_problems_engagement_is_DWTA(self):
        """Asserts that response to community engagement is 'don't want to answer'"""
        prob = NeighbourhoodProblems.objects.create(name=DWTA, short_name='DWTA')
        self.options.update(problems_engagement=[str(prob.id), str(self.neighboourhood_problems.id)])
        form = CommunityEngagementForm(data=self.options)
        self.assertFalse(form.is_valid())
