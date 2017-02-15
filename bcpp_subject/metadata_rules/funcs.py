from edc_constants.constants import POS, NEG, IND, NO, YES, FEMALE, NAIVE
from edc_registration.models import RegisteredSubject

from bcpp.surveys import BCPP_YEAR_3
from member.models import HouseholdMember

from ..models import (
    HicEnrollment, HivTestingHistory, HivResult,
    SexualBehaviour, is_circumcised)
from ..subject_helper import SubjectHelper, DEFAULTER, ON_ART


def is_hic_enrolled(visit_instance):
    """Returns True if subject is enrolled to Hic.
    """
    try:
        HicEnrollment.objects.get(
            subject_visit__subject_identifier=visit_instance.subject_identifier,
            hic_permission=YES)
        return True
    except HicEnrollment.DoesNotExist:
        return False


def func_is_female(visit_instance, *args):
    registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.subject_identifier)
    return registered_subject.gender == FEMALE


def func_requires_recent_partner(visit_instance, *args):
    sexual_behaviour = SexualBehaviour.objects.get(
        subject_visit=visit_instance)
    if sexual_behaviour.last_year_partners:
        return True if sexual_behaviour.last_year_partners >= 1 else False
    return False


def func_requires_second_partner_forms(visit_instance, *args):
    sexual_behaviour = SexualBehaviour.objects.get(
        subject_visit=visit_instance)
    if sexual_behaviour.last_year_partners:
        return True if sexual_behaviour.last_year_partners >= 2 else False
    return False


def func_requires_third_partner_forms(visit_instance, *args):
    sexual_behaviour = SexualBehaviour.objects.get(
        subject_visit=visit_instance)
    if sexual_behaviour.last_year_partners:
        return True if sexual_behaviour.last_year_partners >= 3 else False
    return False


def func_requires_hivlinkagetocare(visit_instance, *args):
    """Returns True is a participant is a defaulter now or at baseline,
    is naive now or at baseline.
    """
    subject_helper = SubjectHelper(visit_instance)
    if subject_helper.defaulter_at_baseline:
        return True
    elif subject_helper.naive_at_baseline:
        return True
    return False


def func_art_defaulter(visit_instance, *args):
    """Returns True is a participant is a defaulter.
    """
    subject_helper = SubjectHelper(visit_instance)
    return subject_helper.final_arv_status == DEFAULTER


def func_art_naive(visit_instance, *args):
    """Returns True if the participant art naive.
    """
    subject_helper = SubjectHelper(visit_instance)
    return subject_helper.final_arv_status == NAIVE


def func_on_art(visit_instance, *args):
    """Returns True if the participant is on art.
    """
    return SubjectHelper(visit_instance).final_arv_status == ON_ART


def func_requires_todays_hiv_result(visit_instance, *args):
    subject_helper = SubjectHelper(visit_instance)
    return subject_helper.final_hiv_status != POS


def func_requires_pima_cd4(visit_instance, *args):
    """Returns True if subject is POS and ART naive.

    Note: if naive at baseline, is also required.
    """
    subject_helper = SubjectHelper(visit_instance)
    return (subject_helper.final_hiv_status == POS
            and (subject_helper.final_arv_status == NAIVE
                 or subject_helper.naive_at_baseline))


def func_known_hiv_pos(visit_instance, *args):
    """Returns True if participant is NOT newly diagnosed POS.
    """
    subject_helper = SubjectHelper(visit_instance)
    return subject_helper.known_positive


def func_requires_hic_enrollment(visit_instance, *args):
    """If the participant is tested HIV NEG and was not HIC
    enrolled then HIC is REQUIRED.

    Not required for last survey / bcpp-year-3.
    """
    if visit_instance.survey_schedule_object.name == BCPP_YEAR_3:
        return False
    subject_helper = SubjectHelper(visit_instance)
    return (subject_helper.final_hiv_status == NEG
            and not is_hic_enrolled(visit_instance))


def func_requires_microtube(visit_instance, *args):
    """Returns True to trigger the Microtube requisition if one is
    """
    # TODO: verify this
    subject_helper = SubjectHelper(visit_instance)
    try:
        hiv_result = HivResult.objects.get(subject_visit=visit_instance)
    except HivResult.DoesNotExist:
        today_hiv_result = None
    else:
        today_hiv_result = hiv_result.hiv_result
    return (
        subject_helper.final_hiv_status != POS
        and not today_hiv_result)


def func_hiv_positive(visit_instance, *args):
    """Returns True if the participant is known or newly
    diagnosed HIV positive.
    """
    return SubjectHelper(visit_instance).final_hiv_status == POS


def func_hiv_indeterminate(visit_instance, *args):
    return SubjectHelper(visit_instance).final_hiv_status == IND


def func_requires_circumcision(visit_instance, *args):
    """Return True if male is not reported as circumcised.
    """
    if visit_instance.household_member.gender == FEMALE:
        return False
    return not is_circumcised(visit_instance)


def func_requires_rbd(visit_instance, *args):
    """Returns True if subject is POS.
    """
    if SubjectHelper(visit_instance).final_hiv_status == POS:
        return True
    return False


def func_requires_vl(visit_instance, *args):
    """Returns True if subject is POS.
    """
    if SubjectHelper(visit_instance).final_hiv_status == POS:
        return True
    return False


def func_requires_hivuntested(visit_instance, *args):
    """Only for ESS."""
    try:
        obj = HivTestingHistory.objects.get(
            subject_visit=visit_instance)
    except:
        pass
    else:
        if obj and obj.has_tested == NO:
            return True
    return False


def func_anonymous_member(visit_instance, *args):
    try:
        household_member = HouseholdMember.objects.get(
            subject_identifier=visit_instance.subject_identifier)
        return household_member.anonymous
    except HouseholdMember.DoesNotExist:
        return False
    except HouseholdMember.MultipleObjectsReturned:
        return False
