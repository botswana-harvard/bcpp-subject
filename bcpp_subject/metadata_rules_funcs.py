from edc_constants.constants import POS, NEG, IND, NO, MALE, YES, FEMALE
from edc_registration.models import RegisteredSubject

from member.models.household_member.household_member import HouseholdMember

from .constants import T1, T2, T3, E0, T0
from .models import (
    Circumcised, HicEnrollment, HivTestingHistory, HivResult,
    SubjectVisit, SexualBehaviour)
from .subject_helper import SubjectHelper


def func_show_recent_partner(visit_instance, *args):
    sexual_behaviour = SexualBehaviour.objects.get(
        subject_visit=visit_instance)
    if sexual_behaviour.last_year_partners:
        return True if sexual_behaviour.last_year_partners >= 1 else False
    return False


def func_show_second_partner_forms(visit_instance, *args):
    sexual_behaviour = SexualBehaviour.objects.get(
        subject_visit=visit_instance)
    if sexual_behaviour.last_year_partners:
        return True if sexual_behaviour.last_year_partners >= 2 else False
    return False


def func_show_third_partner_forms(visit_instance, *args):
    sexual_behaviour = SexualBehaviour.objects.get(
        subject_visit=visit_instance)
    if sexual_behaviour.last_year_partners:
        return True if sexual_behaviour.last_year_partners >= 3 else False
    return False


def is_female(visit_instance, *args):
    registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.subject_identifier)
    return registered_subject.gender == FEMALE


def is_male(visit_instance, *args):
    registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.subject_identifier)
    return registered_subject.gender == MALE


def func_is_baseline_or_ess(visit_instance, *args):
    if visit_instance and visit_instance.visit_code in [E0, T0]:
        return True
    return False


def func_previous_visit(visit_instance, *args):
    if visit_instance.visit_code in [E0, T0]:
        return None
    visit_codes = [T0, T1, T2, T3]
    index = visit_codes.index(visit_instance.visit_code)
    return SubjectVisit.objects.get(
        visit_code=visit_codes[:index][0],
        subject_identifier=visit_instance.subject_identifier)


def func_is_defaulter(visit_instance, *args):
    """Returns True is a participant is a defaulter.
    """
    subject_status_helper = SubjectStatusHelper(
        visit_instance, use_baseline_visit=False)
    return subject_status_helper.defaulter


def func_art_naive(visit_instance, *args):
    """Returns True if the participant is NOT on art or cannot
    be confirmed to be on art.
    """
    subject_status_helper = SubjectStatusHelper(
        visit_instance, use_baseline_visit=False)
    art_naive = (
        not subject_status_helper.on_art and subject_status_helper.hiv_result == POS)
    return art_naive


def func_art_naive_at_annual_or_defaulter(visit_instance, *args):
    previous_visit = func_previous_visit(visit_instance)
    if previous_visit:
        if art_naive_at_enrollment(visit_instance) or func_is_defaulter(previous_visit):
            return True
    elif art_naive_at_enrollment(visit_instance) or func_is_defaulter(visit_instance):
        return True
    else:
        return False


def func_on_art(visit_instance, *args):
    """Returns True if the participant cannot be confirmed to be on art.
    """
    subject_status_helper = SubjectStatusHelper(
        visit_instance, use_baseline_visit=False)
    art_status = (
        subject_status_helper.on_art and subject_status_helper.hiv_result == POS)
    return art_status


def func_requires_pima_vl(visit_instance, *args):
    """Not used.
    """
    # for substudy
    if subject_status_helper.hiv_result == POS and subject_status_helper.art_naive:
        return True
    return False


def func_requires_pima_cd4(visit_instance, *args):
    """Returns True if subject is POS and ART naive.
    """
    # for substudy
    if subject_status_helper.hiv_result == POS and subject_status_helper.art_naive:
        return True
    return False


def func_known_pos(visit_instance, *args):
    """Returns True if participant is NOT a newly diagnosed
    POS as determined by the SubjectStatusHelper.new_pos method.
    """
    subject_status_helper = SubjectStatusHelper(
        visit_instance, use_baseline_visit=False)
    known_pos = subject_status_helper.new_pos is False
    return known_pos


def func_requires_hic_enrollment(visit_instance, *args):
    """If the participant still test HIV NEG and was not HIC
    enrolled then HIC should be REQUIRED.
    """
    if (func_hiv_negative_today(visit_instance)
            and not func_hic_enrolled(visit_instance)):
        return True
    else:
        return False


def func_show_microtube(visit_instance, *args):
    """Returns True to trigger the Microtube requisition if one is
    1. an hic participant who is still HIV-
    2. an hic participant who has sero-converted but the HIV+
       result was not tested by bhp
    3. a new enrollee that is HIV-
     """
    show_micro = False
    if func_hic_enrolled(visit_instance) and not func_pos_tested_by_bhp(visit_instance):
        show_micro = True
    elif not func_hic_enrolled(visit_instance) and not (
            func_hiv_positive_today(visit_instance) or
            known_positive(visit_instance)):
        show_micro = True
    return show_micro


def func_todays_hiv_result_required(visit_instance, *args):
    """Returns True if the an HIV test is required."""
    subject_status_helper = SubjectStatusHelper(
        visit_instance, use_baseline_visit=False)
    if subject_status_helper.todays_hiv_result and not known_positive(visit_instance):
        return True
    if not func_hiv_positive_today(visit_instance) and not known_positive(visit_instance):
        return True
    return False


def func_hiv_negative_today(visit_instance, *args):
    """Returns True if the participant tests negative today.
    """
    hiv_result = SubjectStatusHelper(
        visit_instance, use_baseline_visit=False).hiv_result
    return hiv_result == NEG


def func_hiv_indeterminate_today(visit_instance, *args):
    """Returns True if the participant tests indeterminate today.
    """
    hiv_result = SubjectStatusHelper(
        visit_instance, use_baseline_visit=False).hiv_result
    return hiv_result == IND


def func_hiv_positive_today(visit_instance, *args):
    """Returns True if the participant is known or newly
    diagnosed HIV positive.
    """
    hiv_result = SubjectStatusHelper(
        visit_instance, use_baseline_visit=False).hiv_result
    return hiv_result == POS


# FIXME: this is wrong. SubjectStatusHelper already
# considers the HivResult model
def func_pos_tested_by_bhp(visit_instance, *args):
    """Returns True if the participant is HIV+ and has a POS
    HivResult record.
    """
    hiv_result = SubjectStatusHelper(
        visit_instance, use_baseline_visit=False).hiv_result
    if hiv_result != POS:
        previous_visit = func_previous_visit(visit_instance)
        while previous_visit:
            hiv_result = SubjectStatusHelper(
                previous_visit, use_baseline_visit=False).hiv_result
            if hiv_result == POS:
                break
            previous_visit = func_previous_visit(previous_visit)
    return hiv_result == POS and HivResult.objects.filter(
        subject_visit__subject_identifier=visit_instance.subject_identifier,
        hiv_result=POS).exists()


def func_hiv_positive_today_ahs(visit_instance, *args):
    if func_is_baseline_or_ess(visit_instance):
        return func_hiv_positive_today(visit_instance)
    else:
        # FIXME: why also has to ne on ART??
        if (func_hiv_positive_today(visit_instance)
                and SubjectStatusHelper(visit_instance).on_art):
            return True
    return False


def func_hic_enrolled(visit_instance, *args):
    try:
        HicEnrollment.objects.get(
            subject_visit__subject_identifier=visit_instance.subject_identifier,
            hic_permission=YES)
        return True
    except HicEnrollment.DoesNotExist:
        pass
    return False


# FIXME: does not return
# FIXME: get from helper
def func_rbd_drawn_in_past(visit_instance, *args):
    """Returns the baseline visit instance.
    """
    # FIXME: previous is not baseline!!
    previous_visit = func_previous_visit(visit_instance)
    while previous_visit:
        if SubjectStatusHelper(previous_visit).rbd_sample_drawn:
            return True
        previous_visit = func_previous_visit(previous_visit)
    return False

# FIXME:


def known_positive(visit_instance, *args):
    previous_visit = func_previous_visit(visit_instance)
    while previous_visit:
        if func_hiv_positive_today(previous_visit) or func_known_pos(previous_visit):
            return True
        previous_visit = func_previous_visit(previous_visit)
    return False


def func_no_verbal_hiv_result(visit_instance, *args):
    """Returns True if verbal_hiv_positive response is not
    POS or NEG.
    """
    return SubjectStatusHelper(
        visit_instance).verbal_hiv_result not in ['POS', 'NEG']


def func_requires_circumcision(visit_instance, *args):
    """Return True if male is not reported as circumcised.
    """
    if is_female(visit_instance):
        return False
    elif Circumcised.objects.filter(
            subject_visit__subject_identifier=visit_instance.suject_identifier).exists():
        return False
    return True


# FIXME: REMOVE
def first_enrolled(visit_instance, *args):
    """ Returns true if visit_instance is the visit of first
    enrollment.
    """
    # visit_instance is the visit of first enrollment if no other visit exists
    # prior to it.
    if func_previous_visit(visit_instance):
        return False
    return True


# FIX ME: status helper
def art_naive_at_enrollment(visit_instance, *args):
    previous_visit = func_previous_visit(visit_instance)
    print("visit_instance", visit_instance.visit_code, previous_visit)
    while previous_visit:
        print("first_enrolled(previous_visit)", first_enrolled(previous_visit))
        if first_enrolled(previous_visit) and func_art_naive(previous_visit):
            return True
        previous_visit = func_previous_visit(previous_visit)
    return False


def sero_converter(visit_instance):
    ever_negative = False
    previous_visit = func_previous_visit(visit_instance)
    while previous_visit:
        ever_negative = func_hiv_negative_today(previous_visit)
        if ever_negative:
            break
        previous_visit = func_previous_visit(previous_visit)
    return True if (ever_negative and func_hiv_positive_today(visit_instance)) else False


def func_requires_rbd(visit_instance, *args):
    """Returns True if rdb is required.
    """
    return not SubjectStatusHelper(visit_instance).has_rdb


def func_requires_vl(visit_instance, *args):
    """Returns True if subject is POS.
    """
    if SubjectStatusHelper(visit_instance).final_hiv_status == POS:
        return True
    return False


def func_requires_hivuntested(visit_instance, *args):
    hiv_testing = HivTestingHistory.objects.filter(
        subject_visit__subject_identifier=visit_instance.subject_identifier).last()
    if hiv_testing:
        if hiv_testing.has_tested == NO:
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
