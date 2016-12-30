from django.test import TestCase
from datetime import date

from edc_constants.constants import YES

from ..forms import CommunityEngagementForm
from .test_mixins import SubjectMixin


class TestCommunityEngagementForm(SubjectMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.options = {
            'community_engagement': 'Motshelo',
            'vote_engagement': YES,
            'problems_engagement': YES,
            'problems_engagement_other': None,
            'solve_engagement': YES,
            'problems_engagement': YES,
        }

    def test_valid_form(self):
            """Test to verify whether form will submit"""
            form = CommunityEngagementForm(data=self.data)
            self.assertTrue(form.is_valid())

    def test_if_response_is_DWTA(self):
        self.options.update(the_problems_list=['Don\'t want to answer', 'yes'])
        form = CommunityEngagementForm(data=self.options)
        print(form.errors)
        self.assertFalse(form.is_valid())

    def test_if_response_is_not_DWTA(self):
        self.options.update(the_problems_list=['Don\'t want to answer', 'no'])
        form = CommunityEngagementForm(data=self.options)
        self.assertTrue(form.is_valid())
