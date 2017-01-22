from faker import Faker

from dateutil.relativedelta import relativedelta

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from edc_base.utils import get_utcnow

from member.models import EnrollmentChecklistAnonymous

from ..models.anonymous import AnonymousConsent
from ..models.utils import is_minor

from .enrollment import Enrollment
from .subject_consent import SubjectConsent

fake = Faker()


@receiver(post_delete, weak=False, sender=SubjectConsent, dispatch_uid="subject_consent_on_post_delete")
def subject_consent_on_post_delete(sender, instance, using, **kwargs):
    enrollment = Enrollment.objects.get(
        consent_identifier=instance.consent_identifier)
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
            if created:
                Enrollment.objects.enroll_to_next_survey(
                    subject_identifier=instance.subject_identifier,
                    household_member=instance.household_member,
                    consent_identifier=instance.consent_identifier,
                    report_datetime=instance.report_datetime)


@receiver(post_save, weak=False, sender=EnrollmentChecklistAnonymous,
          dispatch_uid="enrollment_checklist_anonymous_on_post_save")
def enrollment_checklist_anonymous_on_post_save(sender, instance, raw, created, using, **kwargs):
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
                dob=dob,
                identity=identity,
                confirm_identity=identity,
                study_site='88',
                first_name=instance.household_member.first_name,
                initials=instance.household_member.initials,
                may_store_samples=instance.may_store_samples,
                citizen=instance.citizen,
                is_minor=is_minor(dob, instance.created),
                user_created=instance.user_created,
                user_modified=instance.user_modified,
                hostname_created=instance.hostname_created,
                hostname_modified=instance.hostname_modified,
            )


@receiver(post_delete, weak=False, sender=EnrollmentChecklistAnonymous,
          dispatch_uid="enrollment_checklist_anonymous_on_post_delete")
def enrollment_checklist_anonymous_on_post_delete(sender, instance, raw, created, using, **kwargs):
    instance.household_member.anonymousconsent.delete()
    instance.household_member.delete()
