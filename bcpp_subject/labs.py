from edc_lab import AliquotType, LabProfile, ProcessingProfile, RequisitionPanel
from edc_lab.site_labs import site_labs
from edc_lab.lab.processing_profile import Process

from .constants import RESEARCH_BLOOD_DRAW, MICROTUBE, VIRAL_LOAD, ELISA
from .models import SubjectRequisition


lab_profile = LabProfile(
    name='bcpp_subject',
    requisition_model=SubjectRequisition)

pl = AliquotType(name='Plasma', alpha_code='PL', numeric_code='36')

bc = AliquotType(name='Buffy Coat', alpha_code='BC', numeric_code='12')

wb = AliquotType(name='Whole Blood', alpha_code='WB', numeric_code='02')

wb.add_derivatives(bc, pl)

viral_load_processing = ProcessingProfile(name='viral_load', aliquot_type=wb)
vl_pl_process = Process(aliquot_type=pl, aliquot_count=3)
vl_bc_process = Process(aliquot_type=bc, aliquot_count=2)
viral_load_processing.add_processes(vl_pl_process, vl_bc_process)

viral_load_panel = RequisitionPanel(
    name=VIRAL_LOAD,
    model=SubjectRequisition,
    aliquot_type=wb,
    processing_profile=viral_load_processing)
lab_profile.add_panel(viral_load_panel)

microtube_processing = ProcessingProfile(name='microtube', aliquot_type=wb)
microtube_pl_process = Process(aliquot_type=pl, aliquot_count=1)
microtube_bc_process = Process(aliquot_type=bc, aliquot_count=1)
microtube_processing.add_processes(microtube_pl_process, microtube_bc_process)

microtube_panel = RequisitionPanel(
    name=MICROTUBE,
    model=SubjectRequisition,
    aliquot_type=wb,
    processing_profile=microtube_processing)
lab_profile.add_panel(microtube_panel)

elisa_processing = ProcessingProfile(name='elisa', aliquot_type=wb)
elisa_pl_process = Process(aliquot_type=pl, aliquot_count=1)
elisa_processing.add_processes(elisa_pl_process)

elisa_panel = RequisitionPanel(
    name=ELISA,
    model=SubjectRequisition,
    aliquot_type=wb,
    processing_profile=elisa_processing)
lab_profile.add_panel(elisa_panel)

venous_processing = ProcessingProfile(name='venous', aliquot_type=wb)
venous_pl_process = Process(aliquot_type=pl, aliquot_count=2)
venous_bc_process = Process(aliquot_type=bc, aliquot_count=1)
venous_processing.add_processes(venous_pl_process, venous_bc_process)

venous_panel = RequisitionPanel(
    name='Venous (HIV)',
    model=SubjectRequisition,
    aliquot_type=wb,
    processing_profile=venous_processing)
lab_profile.add_panel(venous_panel)

rdb_processing = ProcessingProfile(name='rbd', aliquot_type=wb)
rdb_pl_process = Process(aliquot_type=pl, aliquot_count=4)
rdb_bc_process = Process(aliquot_type=bc, aliquot_count=2)
rdb_processing.add_processes(rdb_pl_process, rdb_bc_process)

rdb_panel = RequisitionPanel(
    name=RESEARCH_BLOOD_DRAW,
    model=SubjectRequisition,
    aliquot_type=wb,
    processing_profile=rdb_processing)
lab_profile.add_panel(rdb_panel)

site_labs.register(lab_profile)
