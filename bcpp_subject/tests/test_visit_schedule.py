import unittest

from ..visit_schedules.crfs_bhs import crfs_bhs
from ..visit_schedules.crfs_ahs import crfs_ahs
from ..visit_schedules.crfs_ess import crfs_ess
from ..visit_schedules.requisitions import requisitions


class TestVisitSchedule(unittest.TestCase):

    def test_ahs_in_intervention(self):
        """Asserts difference in the CRF list between default list
        and AHS intervention map_area."""
        pass

    def test_ahs_in_non_intervention(self):
        """Asserts difference in the CRF list between default list
        and AHS intervention map_area."""
        pass

    # etc ...
