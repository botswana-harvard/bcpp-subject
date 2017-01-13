import unittest

from ..visit_schedules.crfs_ahs import crfs_ahs
from edc_map.site_mappers import site_mappers


class TestVisitSchedule(unittest.TestCase):

    def test_ahs_in_intervention(self):
        """Asserts difference in the CRF list between default list
        and AHS intervention map_area."""
        self.assertTrue(site_mappers.registry['test_community'].intervention)
        for crf in crfs_ahs:
            self.assertFalse('bcpp_subject.hivuntested' == crf.model)

    def test_ahs_in_non_intervention(self):
        """Asserts difference in the CRF list between default list
        and AHS intervention map_area."""
        site_mappers.registry['test_community'].intervention = False
        self.assertFalse(site_mappers.registry['test_community'].intervention)
        for crf in crfs_ahs:
            self.assertTrue(crf.model not in ['bcpp_subject.tbsymptoms', 'bcpp_subject.hivuntested'])
