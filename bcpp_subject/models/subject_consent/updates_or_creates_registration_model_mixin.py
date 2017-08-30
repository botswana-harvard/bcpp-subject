import uuid

from edc_registration.exceptions import RegisteredSubjectError
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin as Base


class UpdatesOrCreatesRegistrationModelMixin(Base):

    @property
    def registration_options(self):
        """Insert internal_identifier to be updated on
        RegisteredSubject.
        """
        registration_options = super().registration_options
        registration_options.update(
            registration_identifier=self.household_member.internal_identifier.hex)
        return registration_options

    def registration_raise_on_illegal_value_change(self, registered_subject):
        """Raises an exception if a value changes between
        updates.
        """
        if registered_subject.identity != self.identity:
            raise RegisteredSubjectError(
                'Identity may not be changed. Expected {}. Got {}'.format(
                    registered_subject.identity,
                    self.identity))
        if (registered_subject.registration_identifier
            and uuid.UUID(registered_subject.registration_identifier) !=
                self.household_member.internal_identifier):
            raise RegisteredSubjectError(
                'Internal Identifier may not be changed. Expected {}. '
                'Got {}'.format(
                    registered_subject.registration_identifier,
                    self.household_member.internal_identifier))
        if registered_subject.dob != self.dob:
            raise RegisteredSubjectError(
                'DoB may not be changed. Expected {}. Got {}'.format(
                    registered_subject.dob,
                    self.dob))

    class Meta:
        abstract = True
