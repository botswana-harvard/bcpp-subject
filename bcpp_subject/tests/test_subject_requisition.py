from django.test import TestCase

from edc_constants.constants import YES

from .test_mixins import SubjectMixin

from ..constants import VIRAL_LOAD, MICROTUBE, RESEARCH_BLOOD_DRAW, ELISA
from ..forms import SubjectRequisitionForm


class TestSubjectRequisitionForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.options = {
            'report_datetime': self.get_utcnow(),
            'subject_visit': self.subject_visit_female.id,
            'panel_name': MICROTUBE,
            'requisition_identifier': 'R1',
            'requisition_datetime': self.get_utcnow(),
            'drawn_datetime': None,
            'is_drawn': YES,
            'reason_not_drawn': None,
            'specimen_identifier': None,
            'study_site': 'Gaborone',
            'specimen_type': 'xxx',
            'item_type': 'tube',
            'item_count': 1,
            'estimated_volume': 4.0,
            'comments': 'good',
        }

    def test_form_is_valid(self):
        subject_requisition_form = SubjectRequisitionForm(data=self.options)
        self.assertTrue(subject_requisition_form.is_valid())
        self.assertTrue(subject_requisition_form.save())

    def test_reason_not_drawn_provided(self):
        self.options.update(reason_not_drawn='refused')
        subject_requisition_form = SubjectRequisitionForm(data=self.options)
        self.assertFalse(subject_requisition_form.is_valid())

    def test_estimated_volume_RBD_less(self):
        """Assert rbd estimated volume is below limit"""
        self.options.update(panel_name=RESEARCH_BLOOD_DRAW)
        subject_requisition_form = SubjectRequisitionForm(data=self.options)
        self.assertFalse(subject_requisition_form.is_valid())

        self.options.update(estimated_volume=9.0)
        subject_requisition_form = SubjectRequisitionForm(data=self.options)
        self.assertTrue(subject_requisition_form.save())

    def test_estimated_volume_RBD_more(self):
        """Assert rbd estimated volume is above limit"""
        self.options.update(panel_name=RESEARCH_BLOOD_DRAW, estimated_volume=15.0)
        subject_requisition_form = SubjectRequisitionForm(data=self.options)
        self.assertFalse(subject_requisition_form.is_valid())

    def test_estimated_volume_viral_load_less(self):
        """Assert viral_load estimated volume is below limit"""
        self.options.update(panel_name=VIRAL_LOAD)
        subject_requisition_form = SubjectRequisitionForm(data=self.options)
        self.assertFalse(subject_requisition_form.is_valid())

        self.options.update(estimated_volume=9.0)
        subject_requisition_form = SubjectRequisitionForm(data=self.options)
        self.assertTrue(subject_requisition_form.save())

    def test_estimated_volume_viral_load_more(self):
        """Assert viral_load estimated volume is above limit"""
        self.options.update(panel_name=VIRAL_LOAD, estimated_volume=15.0)
        subject_requisition_form = SubjectRequisitionForm(data=self.options)
        self.assertFalse(subject_requisition_form.is_valid())

    def test_estimated_volume_microtube_less(self):
        """Assert microtube estimated volume is below limit"""
        self.options.update(panel_name=MICROTUBE, estimated_volume=2)
        subject_requisition_form = SubjectRequisitionForm(data=self.options)
        self.assertFalse(subject_requisition_form.is_valid())

    def test_estimated_volume_microtube_more(self):
        """Assert microtube estimated volume is above limit"""
        self.options.update(panel_name=MICROTUBE, estimated_volume=8.0)
        subject_requisition_form = SubjectRequisitionForm(data=self.options)
        self.assertFalse(subject_requisition_form.is_valid())

    def test_ELISA_panel_name_can_save(self):
        """Assert ELISA panel form can save"""
        self.options.update(panel_name=ELISA)
        subject_requisition_form = SubjectRequisitionForm(data=self.options)

        self.assertTrue(subject_requisition_form.is_valid())
        self.assertTrue(subject_requisition_form.save())

    def test_VENOUS_panel_name_can_save(self):
        """Assert VENOUS panel form can save"""
        self.options.update(panel_name='Venous (HIV)')
        subject_requisition_form = SubjectRequisitionForm(data=self.options)
        self.assertTrue(subject_requisition_form.save())
