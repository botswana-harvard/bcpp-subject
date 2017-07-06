from edc_visit_schedule.visit import Requisition

from ..labs import rdb_panel, microtube_panel, viral_load_panel
from ..labs import venous_panel, elisa_panel

requisitions = (
    Requisition(
        show_order=10, model='bcpp_subject.subjectrequisition',
        panel=rdb_panel, required=False, additional=False),
    Requisition(
        show_order=20, model='bcpp_subject.subjectrequisition',
        panel=viral_load_panel, required=False, additional=False),
    Requisition(
        show_order=30, model='bcpp_subject.subjectrequisition',
        panel=microtube_panel, required=False, additional=False),
    Requisition(
        show_order=40, model='bcpp_subject.subjectrequisition',
        panel=venous_panel, required=False, additional=False),
    Requisition(
        show_order=50, model='bcpp_subject.subjectrequisition',
        panel=elisa_panel, required=False, additional=False)
)
