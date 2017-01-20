from django.db.models.signals import post_save, post_delete

from django.db import transaction
from django.dispatch import receiver

from django.db.utils import IntegrityError

from ..exceptions import EnrollmentError

from .enrollment import EnrollmentAhs, EnrollmentBhs, EnrollmentEss
from .subject_consent import SubjectConsent
from .utils import get_enrollment_model_class
from builtins import issubclass
from bcpp_subject.models.anonymous.anonymous_consent import AnonymousConsent


@receiver(post_delete, weak=False, dispatch_uid="enrollment_on_post_delete")
def enrollment_on_post_delete(sender, instance, using, **kwargs):
    if sender in [EnrollmentAhs, EnrollmentBhs, EnrollmentEss]:
        instance.household_member.is_consented = False
        instance.household_member.save()


@receiver(post_delete, weak=False, sender=SubjectConsent, dispatch_uid="subject_consent_on_post_delete")
def subject_consent_on_post_delete(sender, instance, using, **kwargs):
    EnrollmentModelClass = get_enrollment_model_class(instance)
    enrollment = EnrollmentModelClass.objects.get(subject_identifier=instance.subject_identifier)
    enrollment.delete()
    instance.household_member.is_consented = False
    instance.household_member.save()


@receiver(post_save, weak=False, dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if issubclass(sender, (SubjectConsent, AnonymousConsent)):
            # update household member field attrs
            instance.household_member.is_consented = True
            instance.household_member.absent = False
            instance.household_member.undecided = False
            instance.household_member.refused = False
            instance.household_member.subject_identifier = instance.subject_identifier
            instance.household_member.save()
            instance.household_member.household_structure.enrolled = True
            instance.household_member.household_structure.save()

            # auto-complete an enrollment. Enrollment will create appointments
            EnrollmentModelClass = get_enrollment_model_class(instance)
            try:
                enrollment = EnrollmentModelClass.objects.get(
                    subject_identifier=instance.subject_identifier)
            except EnrollmentModelClass.DoesNotExist:
                with transaction.atomic():
                    try:
                        EnrollmentModelClass.objects.create(
                            subject_identifier=instance.subject_identifier,
                            household_member=instance.household_member,
                            report_datetime=instance.report_datetime,
                            survey=instance.survey_object.field_value,
                            survey_schedule=instance.survey_schedule_object.field_value,
                            is_eligible=True)
                    except IntegrityError as e:
                        raise EnrollmentError(str(e))
            else:
                enrollment.save()
