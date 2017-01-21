from survey import S

from bcpp.surveys import BHS_SURVEY, AHS_SURVEY, ESS_SURVEY, ANONYMOUS_SURVEY

from ..exceptions import ConsentError, EnrollmentError

from .enrollment import EnrollmentBhs, EnrollmentAhs, EnrollmentEss, EnrollmentAno


def get_enrollment_model_class(instance):
    EnrollmentModelClass = None
    try:
        survey_name = instance.survey_object.name
    except AttributeError:
        raise ConsentError(
            'Survey has not been set for survey_schedule {}.'.format(
                instance.survey_schedule_object.field_value))

    if survey_name == BHS_SURVEY:
        EnrollmentModelClass = EnrollmentBhs
    elif survey_name == AHS_SURVEY:
        EnrollmentModelClass = EnrollmentAhs
    elif survey_name == ESS_SURVEY:
        EnrollmentModelClass = EnrollmentEss
    elif survey_name == ANONYMOUS_SURVEY:
        EnrollmentModelClass = EnrollmentAno
    else:
        raise EnrollmentError(
            'Unable to determine the Enrollment Model from {}. '
            'Got survey = {}.'.format(
                instance._meta.label_lower, survey_name))
    return EnrollmentModelClass


def get_enrollment_survey(consents=None, survey_schedule_object=None):
    """Returns the survey field value based on whether or not
    subject with this identity has ever been consented."""
    if consents:
        survey = AHS_SURVEY
    else:
        survey = ESS_SURVEY
    return S(survey_schedule_object.field_value, survey_name=survey).survey_field_value
