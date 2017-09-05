from bcpp_referral.bcpp_referral_facilities import bcpp_referral_facilities
from bcpp_referral.referral import Referral
from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES
from faker import Faker
from member.models import EnrollmentChecklistAnonymous, EnrollmentChecklist
from member.models import EnrollmentLoss, HouseholdMember

from ..models.anonymous import AnonymousConsent
from ..models.utils import is_minor
from .enrollment import Enrollment
from .subject_consent import SubjectConsent
from .subject_referral import SubjectReferral

fake = Faker()
post_delete.providing_args = set(["instance", "using", "raw"])


@receiver(post_save, weak=False, sender=SubjectReferral,
          dispatch_uid='referral_on_post_save')
def referral_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        try:
            subject_visit = instance.subject_visit
        except AttributeError:
            pass
        else:
            referral = Referral(
                subject_visit=subject_visit,
                referral_facilities=bcpp_referral_facilities)
            for field in sender._meta.get_fields():
                try:
                    value = getattr(referral, field.name)
                except AttributeError:
                    pass
                else:
                    setattr(instance, field.name, value)
            instance.referral_appt_date = referral.referral_appt_datetime
            instance.scheduled_appt_date = referral.scheduled_appt_datetime
            try:
                if not instance.referral_code:
                    instance.referral_code = 'pending'
            except AttributeError:
                pass


@receiver(post_delete, weak=False, sender=SubjectConsent,
          dispatch_uid="subject_consent_on_post_delete")
def subject_consent_on_post_delete(sender, instance, raw, using, **kwargs):
    if not raw:
        try:
            enrollment = Enrollment.objects.get(
                consent_identifier=instance.consent_identifier)
        except Enrollment.DoesNotExist:
            pass
        else:
            enrollment.delete()


@receiver(post_save, weak=False, dispatch_uid='consent_on_post_save')
def consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if issubclass(sender, (SubjectConsent, AnonymousConsent)):
            # update household member field attrs
            instance.household_member.absent = False
            instance.household_member.undecided = False
            instance.household_member.refused = False
            instance.household_member.subject_identifier = instance.subject_identifier
            instance.household_member.save()
            instance.household_member.household_structure.enrolled = True
            instance.household_member.household_structure.save()

            # auto-complete an enrollment. Enrollment will create appointments
            if created:
                Enrollment.objects.enroll_to_next_survey(
                    subject_identifier=instance.subject_identifier,
                    household_member=instance.household_member,
                    consent_identifier=instance.consent_identifier,
                    report_datetime=instance.report_datetime)


@receiver(post_save, weak=False, sender=EnrollmentChecklistAnonymous,
          dispatch_uid="enrollment_checklist_anonymous_on_post_save")
def enrollment_checklist_anonymous_on_post_save(
        sender, instance, raw, created, using, **kwargs):
    if not raw:
        if created:
            # update HHM attrs
            instance.household_member.enrollment_checklist_completed = True
            instance.household_member.save()
            # fill in consent
            identity = fake.credit_card_number()
            dob = (instance.household_member.created
                   - relativedelta(years=instance.age_in_years))
            AnonymousConsent.objects.create(
                household_member=instance.household_member,
                consent_datetime=get_utcnow(),
                gender=instance.gender,
                dob=dob.date(),
                citizen=NO,
                identity=identity,
                confirm_identity=identity,
                study_site='88',
                first_name=instance.household_member.first_name,
                initials=instance.household_member.initials,
                may_store_samples=instance.may_store_samples,
                is_minor=is_minor(dob, instance.created),
                user_created=instance.user_created,
                user_modified=instance.user_modified,
                hostname_created=instance.hostname_created,
                hostname_modified=instance.hostname_modified,
            )


@receiver(post_delete, weak=False, sender=EnrollmentChecklistAnonymous,
          dispatch_uid="enrollment_checklist_anonymous_on_post_delete")
def enrollment_checklist_anonymous_on_post_delete(
        sender, instance, raw, created, using, **kwargs):
    if not raw:
        instance.household_member.anonymousconsent.delete()
        instance.household_member.delete()


@receiver(post_save, weak=False, sender=EnrollmentChecklist,
          dispatch_uid="enrollment_checklist_on_post_save")
def enrollment_checklist_on_post_save(
        sender, instance, raw, created, using, **kwargs):
    """Updates adds or removes the Loss form and updates
    household_member.
    """
    if not raw:
        if not instance.is_eligible:
            try:
                enrollment_loss = EnrollmentLoss.objects.using(using).get(
                    household_member=instance.household_member)
                enrollment_loss.report_datetime = instance.report_datetime
                enrollment_loss.reason = instance.loss_reason
                enrollment_loss.save()
            except EnrollmentLoss.DoesNotExist:
                enrollment_loss = EnrollmentLoss(
                    household_member=instance.household_member,
                    report_datetime=instance.report_datetime,
                    reason=instance.loss_reason)
                enrollment_loss.save()
            instance.household_member.eligible_subject = False
        else:
            enrollment_loss = EnrollmentLoss.objects.filter(
                household_member=instance.household_member).delete()
            instance.household_member.eligible_subject = True
        instance.household_member.enrollment_checklist_completed = True

        if created:
            instance.household_member.visit_attempts += 1
        instance.household_member.non_citizen = instance.non_citizen
        instance.household_member.citizen = instance.citizen == YES
        instance.household_member.spouse_of_citizen = (
            instance.citizen == NO
            and instance.legal_marriage == YES
            and instance.marriage_certificate == YES)
        instance.household_member.save()

        if created:
            household_member = HouseholdMember.objects.get(
                pk=instance.household_member.pk)
            if household_member.consent:
                Enrollment.objects.enroll_to_next_survey(
                    subject_identifier=household_member.subject_identifier,
                    household_member=household_member,
                    consent_identifier=household_member.consent.consent_identifier,
                    report_datetime=instance.report_datetime)


@receiver(post_delete, weak=False, sender=EnrollmentChecklist,
          dispatch_uid="enrollment_checklist_on_post_delete")
def enrollment_checklist_on_post_delete(sender, instance, using, raw, **kwargs):
    if not raw:
        EnrollmentLoss.objects.filter(
            household_member=instance.household_member).delete()
        instance.household_member.enrollment_checklist_completed = False
        instance.household_member.eligible_subject = False
        instance.household_member.visit_attempts -= 1
        if instance.household_member.visit_attempts < 0:
            instance.household_member.visit_attempts = 0
        instance.household_member.appointment_set.all().delete()
        instance.household_member.save()
