from edc_constants.constants import POS, NEG, IND, NO, MALE, YES, FEMALE
from edc_registration.models import RegisteredSubject

from .constants import DECLINED, T0
from .models import (
    Circumcised, HicEnrollment, HivTestingHistory, HivResult)
from .subject_status_helper import SubjectStatusHelper


def is_female(visit_instance, *args):
    registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.subject_identifier)
    return registered_subject.gender == FEMALE


def is_male(visit_instance, *args):
    registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.subject_identifier)
    return registered_subject.gender == MALE


def func_is_baseline(visit_instance, *args):
    if visit_instance and visit_instance.visit_code == T0:
        return True
    return False


def func_is_annual(visit_instance, *args):
    # FIXME: THIS IS too simple,  in context of having ESS
    if visit_instance.code != T0:
        return True
    return False


def func_is_defaulter(visit_instance, *args):
    """Returns True is a participant is a defaulter."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
    return subject_status_helper.defaulter


def func_art_naive(visit_instance, *args):
    """Returns True if the participant is NOT on art or cannot
    be confirmed to be on art."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
    art_naive = not subject_status_helper.on_art and subject_status_helper.hiv_result == POS
    return art_naive


def func_art_naive_at_annual_or_defaulter(visit_instance, *args):
    if visit_instance.previous_visit:
        if art_naive_at_enrollment(visit_instance) or func_is_defaulter(visit_instance.previous_visit):
            return True
    elif art_naive_at_enrollment(visit_instance) or func_is_defaulter(visit_instance):
        return True
    else:
        return False


def func_on_art(visit_instance, *args):
    """Returns True if the participant cannot be confirmed to be on art."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
    art_status = subject_status_helper.on_art and subject_status_helper.hiv_result == POS
    return art_status


def func_rbd_ahs(visit_instance, *args):
    """Returns True if the participant is on art at ahs"""
    if not func_is_baseline(visit_instance):
        if func_hiv_negative_today(visit_instance.previous_visit):
            return False
        else:
            return True
    else:
        return False


def func_require_pima(visit_instance, *args):
    """Returns True or False for doing PIMA based on hiv status and art status at each survey."""
    if func_is_baseline(visit_instance) and func_art_naive(visit_instance):
        return True
    elif sero_converter(visit_instance) and func_art_naive(visit_instance):
        return True
    elif art_naive_at_enrollment(visit_instance):
        return True
    return False


def func_known_pos(visit_instance, *args):
    """Returns True if participant is NOT a newly diagnosed POS as determined
    by the SubjectStatusHelper.new_pos method."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
    known_pos = subject_status_helper.new_pos is False
    return known_pos


def func_is_circumcision(visit_instance, *args):
    try:
        Circumcised.objects.get(subject_visit=visit_instance.previous_visit)
    except Circumcised.DoesNotExist:
        return False
    return True


def func_show_hic_enrollment(visit_instance, *args):
    """ If the participant still test HIV NEG and was not HIC enrolled then HIC should be REQUIRED. """
    if func_hiv_negative_today(visit_instance) and not func_hic_enrolled(visit_instance):
        return True
    else:
        return False


def func_show_microtube(visit_instance, *args):
    """Returns True to trigger the Microtube requisition if one is
    1. an hic participant who is still HIV-
    2. an hic participant who has sero-converted but the HIV+ result was not tested by bhp
    3. a new enrollee that is HIV-
     """
    show_micro = False
    if func_hic_enrolled(visit_instance) and not func_pos_tested_by_bhp(visit_instance):
        show_micro = True
    elif not func_hic_enrolled(visit_instance) and not (func_hiv_positive_today(visit_instance) or
                                                        func_known_pos_in_prev_year(visit_instance)):
        show_micro = True
    return show_micro


def func_todays_hiv_result_required(visit_instance, *args):
    """Returns True if the an HIV test is required."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
    if subject_status_helper.todays_hiv_result and not func_known_pos_in_prev_year(visit_instance):
        return True
    if not func_hiv_positive_today(visit_instance) and not func_known_pos_in_prev_year(visit_instance):
        return True
    return False


def func_hiv_negative_today(visit_instance, *args):
    """Returns True if the participant tests negative today."""
    hiv_result = SubjectStatusHelper(visit_instance, use_baseline_visit=False).hiv_result
    return hiv_result == NEG


def func_hiv_indeterminate_today(visit_instance, *args):
    """Returns True if the participant tests indeterminate today."""
    hiv_result = SubjectStatusHelper(visit_instance, use_baseline_visit=False).hiv_result
    return hiv_result == IND


def func_hiv_positive_today(visit_instance, *args):
    """Returns True if the participant is known or newly diagnosed HIV positive."""
    hiv_result = SubjectStatusHelper(visit_instance, use_baseline_visit=False).hiv_result
    return hiv_result == POS


def func_pos_tested_by_bhp(visit_instance, *args):
    """Returns True if the participant is HIV+ and has a POS HivResult record."""
    hiv_result = SubjectStatusHelper(visit_instance, use_baseline_visit=False).hiv_result
    if hiv_result != POS:
        previous_visit = visit_instance.previous_visit
        while previous_visit:
            hiv_result = SubjectStatusHelper(previous_visit, use_baseline_visit=False).hiv_result
            if hiv_result == POS:
                break
            previous_visit = previous_visit.previous_visit
    return hiv_result == POS and HivResult.objects.filter(
        subject_visit__subject_identifier=visit_instance.subject_identifier,
        hiv_result=POS).exists()


def func_hiv_positive_today_ahs(visit_instance, *args):
    if func_is_baseline(visit_instance):
        return func_hiv_positive_today(visit_instance)
    else:
        # FIXME: why also has to ne on ART??
        if func_hiv_positive_today(visit_instance) and SubjectStatusHelper(visit_instance).on_art:
            return True
    return False


def func_hic_enrolled(visit_instance, *args):
    try:
        HicEnrollment.objects.get(subject_visit=visit_instance, hic_permission=YES)
        return True
    except HicEnrollment.DoesNotExist:
        previous_visit = visit_instance.previous_visit
        while previous_visit:
            try:
                HicEnrollment.objects.get(subject_visit=previous_visit, hic_permission=YES)
                return True
            except HicEnrollment.DoesNotExist:
                pass
            previous_visit = previous_visit.previous_visit
    return False


def func_hiv_result_neg_baseline(visit_instance, *args):
    """ Returns HIV negative result """
    subject_status_helper = SubjectStatusHelper(visit_instance.previous_visit)
    return True if subject_status_helper.hiv_result == NEG else False


def func_hiv_neg_bhs(visit_instance, *args):
    if func_is_baseline(visit_instance):
        previous_visit = visit_instance
    else:
        previous_visit = visit_instance.previous_visit
    subject_status_helper = SubjectStatusHelper(previous_visit)
    return True if subject_status_helper.hiv_result == NEG else False


def func_baseline_hiv_positive_today(visit_instance, *args):
    """Returns the baseline visit instance."""
    return SubjectStatusHelper(visit_instance, use_baseline_visit=True).hiv_result == POS


def func_baseline_hiv_positive_and_documentation_pos(visit_instance, *args):
    """Returns the baseline visit instance."""
    subject_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=True)
    return (subject_helper.hiv_result == POS and
            subject_helper.direct_hiv_pos_documentation or
            not subject_helper.direct_hiv_pos_documentation)


def func_baseline_hiv_positive_and_not_on_art(visit_instance, *args):
    """Returns the baseline visit instance."""
    # FIXME: previous is not baseline!!
    baseline_visit_instance = visit_instance.previous_visit
    subject_helper = SubjectStatusHelper(baseline_visit_instance)
    return subject_helper.hiv_result == POS and not subject_helper.on_art


def func_baseline_pos_and_testreview_documentation_pos(visit_instance, *args):
    """Returns the baseline visit instance."""
    subject_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=True)
    return subject_helper.hiv_result == POS and subject_helper.direct_hiv_pos_documentation


def func_baseline_vl_drawn(visit_instance, *args):
    """Returns the baseline visit instance."""
    return SubjectStatusHelper(visit_instance, use_baseline_visit=True).vl_sample_drawn


def func_rbd_drawn_in_past(visit_instance, *args):
    """Returns the baseline visit instance."""
    # FIXME: previous is not baseline!!
    previous_visit = visit_instance.previous_visit
    while previous_visit:
        if SubjectStatusHelper(previous_visit).rbd_sample_drawn:
            return True
        previous_visit = previous_visit.previous_visit
    return False


def func_baseline_pima_keyed(visit_instance, *args):
    return SubjectStatusHelper(visit_instance, use_baseline_visit=True).pima_instance


def func_baseline_hiv_care_adherance_keyed(visit_instance, *args):
    return SubjectStatusHelper(visit_instance, use_baseline_visit=True).hiv_care_adherence_instance


def func_not_required(visit_instance, *args):
    """Returns True (always)."""
    return True


def func_known_pos_in_prev_year(visit_instance, *args):
    previous_visit = visit_instance.previous_visit
    while previous_visit:
        if func_hiv_positive_today(previous_visit) or func_known_pos(previous_visit):
            return True
        previous_visit = previous_visit.previous_visit
    return False


def func_no_verbal_hiv_result(visit_instance, *args):
    """Returns True if verbal_hiv_positive response is not POS or NEG."""
    return SubjectStatusHelper(visit_instance).verbal_hiv_result not in ['POS', 'NEG']


def func_circumcision_not_required(visit_instance, *args):
    return is_female(visit_instance) or func_is_circumcision(visit_instance)


def first_enrolled(visit_instance, *args):
    """ Returns true if visit_instance is the visit of first enrollment. """
    # visit_instance is the visit of first enrollment if no other visit exists prior to it.
    if visit_instance.previous_visit:
        return False
    return True


def art_naive_at_enrollment(visit_instance, *args):
    previous_visit = visit_instance.previous_visit
    while previous_visit:
        if first_enrolled(previous_visit) and func_art_naive(previous_visit):
            return True
        previous_visit = previous_visit.previous_visit
    return False


def sero_converter(visit_instance):
    ever_negative = False
    previous_visit = visit_instance.previous_visit
    while previous_visit:
        ever_negative = func_hiv_negative_today(previous_visit)
        if ever_negative:
            break
        previous_visit = previous_visit.previous_visit
    return True if (ever_negative and func_hiv_positive_today(visit_instance)) else False


def func_rbd(visit_instance, *args):
    """Returns True or False to indicate a participant should be offered an rbd."""
    # if pos at bhs then return true
    if func_hiv_positive_today(visit_instance) and not func_rbd_drawn_in_past(visit_instance):
        return True
    return False


def func_vl(visit_instance, *args):
    """Returns True  or False to indicate participant needs to be offered a viral load."""

    if func_is_baseline(visit_instance):
        return func_hiv_positive_today(visit_instance)
    # Hiv+ve at enrollment, art naive at enrollment
    elif art_naive_at_enrollment(visit_instance):
        return True
    # Hiv -ve at enrollment and seroconverted
    elif sero_converter(visit_instance):
        return True
    elif func_hiv_positive_today(visit_instance):
        helper = SubjectStatusHelper(visit_instance.previous_visit, use_baseline_visit=True)
        try:
            if helper.hiv_result == DECLINED:
                return True
        except AttributeError:
            pass
    return False


def func_poc_vl(visit_instance, *args):
    """Returns True or False to indicate participant needs to be offered a POC viral load."""
    if func_art_naive(visit_instance):
        return True
    return False


def hiv_testing_history(visit_instance, *args):
    try:
        hiv_testing = HivTestingHistory.objects.get(subject_visit=visit_instance)
    except HivTestingHistory.DoesNotExist:
        return False
    return hiv_testing.has_tested == NO


def func_hiv_untested(visit_instance, *args):
    if func_is_baseline(visit_instance):
        return hiv_testing_history(visit_instance)
    return False
