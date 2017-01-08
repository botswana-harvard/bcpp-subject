from django.test import TestCase, tag

from django.views.generic.base import TemplateView
from django.test.client import RequestFactory

from ..views import DashboardView
from ..views.dashboard_view import BcppDashboardExtraFieldMixin

from .test_mixins import SubjectMixin


@tag('me2')
class TestDashboard(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.visit = self.make_subject_visit_for_consented_subject(
            'T0', report_datetime=self.get_utcnow())
        self.appointment = self.visit.appointment
        self.subject_identifier = self.appointment.subject_identifier
        self.household_member = self.visit.household_member
        self.appointments = self.visit.appointment.__class__.objects.filter(
            subject_identifier=self.subject_identifier)
        self.request = RequestFactory().get('/')
        self.request.user = 'erik'

    def test_survey(self):

        class Dummy(BcppDashboardExtraFieldMixin, TemplateView):
            template_name = 'bcpp_subject/dashboard.html'

        survey_object = self.household_member.household_structure.survey_object
        kwargs = {
            'subject_identifier': self.subject_identifier,
            'survey': survey_object.field_value}
        response = Dummy.as_view()(self.request, **kwargs)
        self.assertEqual(
            response.context_data.get('survey'), survey_object)

    def test_household_member(self):

        class Dummy(BcppDashboardExtraFieldMixin, TemplateView):
            template_name = 'bcpp_subject/dashboard.html'

        survey_object = self.household_member.household_structure.survey_object
        kwargs = {
            'subject_identifier': self.subject_identifier,
            'survey': survey_object.field_value,
            'household_member': self.household_member.id}
        response = Dummy.as_view()(self.request, **kwargs)
        self.assertEqual(
            response.context_data.get('household_member'), self.household_member)

    def test_appointments(self):

        class Dummy(BcppDashboardExtraFieldMixin, TemplateView):
            template_name = 'bcpp_subject/dashboard.html'

        survey_object = self.household_member.household_structure.survey_object
        kwargs = {
            'subject_identifier': self.subject_identifier,
            'survey': survey_object.field_value,
            'household_member': self.household_member.id,
            'appointment': self.appointment.id}
        response = Dummy.as_view()(self.request, **kwargs)
        self.assertEqual(
            len(response.context_data.get('apppointments')),
            self.apppointments.count())
        self.assertEqual(
            response.context_data.get('apppointment'),
            self.apppointments)

    def test_survey2(self):
        class Dummy(DashboardView, TemplateView):
            template_name = 'bcpp_subject/dashboard.html'

        survey_object = self.household_member.household_structure.survey_object
        kwargs = {
            'subject_identifier': self.subject_identifier,
            'survey_name': survey_object.field_value}
        response = Dummy.as_view()(self.request, **kwargs)
        self.assertEqual(
            response.context_data.get('survey_name'), survey_object.field_value)
        self.assertEqual(
            response.context_data.get('survey'), survey_object)
