from django.apps import apps as django_apps
from django.core.management.base import BaseCommand

from bcpp_subject.models import SubjectConsent, Appointment, EnrollmentAhs
from edc_map.models import InnerContainer
from member.models import HouseholdMember


def re_save_enrollement(subject_identifier=None):
    """Resave enrollment to create missing appointments.
    """
    try:
        enrollment = EnrollmentAhs.objects.get(
            subject_identifier=subject_identifier)
    except EnrollmentAhs.DoesNotExist:
        pass
    else:
        enrollment.save()


def plot_identifiers(map_area=None):
    """Returns a list of plot identifiers allocated to this device.
    """
    edc_device_app_config = django_apps.get_app_config('edc_device')
    device_id = edc_device_app_config.device_id
    plot_identifiers = []
    try:
        plot_identifiers = InnerContainer.objects.get(
            device_id=device_id,
            map_area=map_area).identifier_labels
    except InnerContainer.DoesNotExist:
        pass
    return plot_identifiers


class Command(BaseCommand):

    help = 'Create missing appointments.'

    def add_arguments(self, parser):
        parser.add_argument('map_area', type=str, help='map_area')

    def handle(self, *args, **options):
        map_area = options['map_area']
        survey_schedule = f'bcpp-survey.bcpp-year-3.{map_area}'
        dispatched_plot_identifiers = plot_identifiers(map_area=map_area)
        household_members = HouseholdMember.objects.filter(
            household_structure__household__plot__map_area=map_area,
            household_structure__household__plot__plot_identifier__in=dispatched_plot_identifiers,
            survey_schedule=survey_schedule)
        for household_member in household_members:
            subject_consent = SubjectConsent.objects.filter(
                subject_identifier=household_member.subject_identifier)
            if subject_consent:
                try:
                    Appointment.objects.get(
                        household_member=household_member,
                        visit_code='T2')
                except Appointment.DoesNotExist:
                    re_save_enrollement(
                        subject_identifier=household_member.subject_identifier)
                    self.stdout.write(self.style.SUCCESS(
                        f'Succefully created an appoint for {household_member.subject_identifier}.'))
