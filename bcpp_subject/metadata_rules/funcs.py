from edc_constants.constants import POS, NEG, IND, NO, MALE, YES, FEMALE, NAIVE,\
    DECLINED
from edc_registration.models import RegisteredSubject

from member.models import HouseholdMember

# from .constants import T1, T2, T3, E0, T0
from ..labs import rdb_panel
from ..models import (
    HicEnrollment, HivTestingHistory,
    SexualBehaviour, SubjectRequisition, is_circumcised)
from ..subject_helper import SubjectHelper, DEFAULTER, ON_ART
from bcpp_subject.constants import NOT_PERFORMED


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


def is_female(visit_instance, *args):
    registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.subject_identifier)
    return registered_subject.gender == FEMALE


def is_male(visit_instance, *args):
    registered_subject = RegisteredSubject.objects.get(
        subject_identifier=visit_instance.subject_identifier)
    return registered_subject.gender == MALE


def func_art_defaulter(visit_instance, *args):
    """Returns True is a participant is a defaulter.
    """
    return SubjectHelper(visit_instance).final_arv_status == DEFAULTER


def func_art_naive(visit_instance, *args):
    """Returns True if the participant art naive.
    """
    subject_helper = SubjectHelper(visit_instance)
    return (subject_helper.final_arv_status == NAIVE or
            subject_helper.naive_at_enrollment)


def func_on_art(visit_instance, *args):
    """Returns True if the participant is on art.
    """
    return SubjectHelper(visit_instance).final_arv_status == ON_ART


def func_requires_todays_hiv_result(visit_instance, *args):
    subject_helper = SubjectHelper(visit_instance)
    return (subject_helper.final_hiv_status != POS)


def func_requires_pima_cd4(visit_instance, *args):
    """Returns True if subject is POS and ART naive.
    """
    subject_helper = SubjectHelper(visit_instance)
    return (subject_helper.final_hiv_status == POS
            and (subject_helper.final_arv_status == NAIVE
                 or subject_helper.naive_at_enrollment))


def func_known_hiv_pos(visit_instance, *args):
    """Returns True if participant is NOT newly diagnosed POS.
    """
    subject_helper = SubjectHelper(visit_instance)
    return subject_helper.known_positive


def func_requires_hic_enrollment(visit_instance, *args):
    """If the participant is tested HIV NEG and was not HIC
    enrolled then HIC is REQUIRED.
    """
    subject_helper = SubjectHelper(visit_instance)
    return (subject_helper.final_hiv_status == NEG
            and not func_hic_enrolled(visit_instance))


def func_requires_microtube(visit_instance, *args):
    """Returns True to trigger the Microtube requisition if one is
    1. an hic participant who is still HIV-
    2. an hic participant who has sero-converted but the HIV+
       result was not tested by bhp
    3. a new enrollee that is HIV-
     """
    # TODO: verify this
    subject_helper = SubjectHelper(visit_instance)
    return (
        SubjectHelper(visit_instance).final_hiv_status != POS
        and subject_helper.raw.today_hiv_result)


def func_hiv_positive(visit_instance, *args):
    """Returns True if the participant is known or newly
    diagnosed HIV positive.
    """
    return SubjectHelper(visit_instance).final_hiv_status == POS


def func_hiv_indeterminate(visit_instance, *args):
    return SubjectHelper(visit_instance).final_hiv_status == IND


def func_hic_enrolled(visit_instance, *args):
    try:
        HicEnrollment.objects.get(
            subject_visit__subject_identifier=visit_instance.subject_identifier,
            hic_permission=YES)
        return True
    except HicEnrollment.DoesNotExist:
        return False


def func_requires_circumcision(visit_instance, *args):
    """Return True if male is not reported as circumcised.
    """
    if visit_instance.household_member.gender == FEMALE:
        return False
    return not is_circumcised(visit_instance)


def func_requires_rbd(visit_instance, *args):
    """Returns True if rdb is required.
    """
    requires_rbd = False
    if SubjectHelper(visit_instance).final_hiv_status == POS:
        try:
            SubjectRequisition.objects.get(
                subject_visit__subject_identifier=visit_instance.subject_identifier,
                panel_name=rdb_panel.name)
        except SubjectRequisition.DoesNotExist:
            requires_rbd = True
    return requires_rbd


def func_requires_vl(visit_instance, *args):
    """Returns True if subject is POS.
    """
    if SubjectHelper(visit_instance).final_hiv_status == POS:
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
