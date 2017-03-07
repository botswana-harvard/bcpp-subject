from edc_base.utils import age
from edc_constants.constants import YES

from .circumcision import Circumcision


def is_minor(dob, reference_datetime):
    return 16 <= age(dob, reference_datetime).years < 18


def is_circumcised(visit_instance):
    """Returns True if circumcised before or at visit
    report datetime.
    """
    is_circumcised = Circumcision.objects.filter(
        subject_visit__subject_identifier=visit_instance.subject_identifier,
        subject_visit__report_datetime__lte=visit_instance.report_datetime,
        circumcised=YES).exists()
    return is_circumcised
