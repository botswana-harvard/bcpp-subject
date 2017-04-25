

def rbd_household_member(identity=None):
        """Returns a household_member instance if identity matches for a
        household in 0000-00 or None.
        """
        try:
            registered_subject = RegisteredSubject.objects.get(identity=identity)
        except RegisteredSubject.DoesNotExist:
            rbd_household_member = None
        else:
            try:
                rbd_household_member = HouseholdMember.objects.get(
                    internal_identifier=registered_subject.registration_identifier,
                    household_structure__household__plot__plot_identifier__endswith='0000-00')
            except HouseholdMember.DoesNotExist:
                rbd_household_member = None
        return rbd_household_member