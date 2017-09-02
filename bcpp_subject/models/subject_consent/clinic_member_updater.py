from django.core.exceptions import ObjectDoesNotExist
from edc_registration.models import RegisteredSubject
from member.models import HouseholdMember


class ClinicMemberUpdater:

    """A class to update the clinic household member if it already
    exists queried on the identity/OMANG.
    """

    plot_identifier_suffix = '0000-00'

    def __init__(self, model_obj=None):
        try:
            registered_subject = RegisteredSubject.objects.get(
                identity=model_obj.identity)
        except RegisteredSubject.DoesNotExist:
            registered_subject = None
        else:
            try:
                household_member = HouseholdMember.objects.get(
                    internal_identifier=registered_subject.registration_identifier,
                    household_structure__household__plot__plot_identifier__endswith=self.plot_identifier_suffix)
            except ObjectDoesNotExist:
                pass
            else:
                household_member.internal_identifier = model_obj.household_member.internal_identifier
                household_member.save()
