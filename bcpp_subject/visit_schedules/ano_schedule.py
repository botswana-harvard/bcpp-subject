from edc_visit_schedule.schedule import Schedule

from .crfs_ess import crfs_ess
from .requisitions import requisitions

ano_schedule = Schedule(name='ano_schedule', title='Anonymous')

ano_schedule.add_visit(
    code='A0',
    title='Anonymous Survey',
    timepoint=0,
    base_interval=0,
    requisitions=requisitions,
    crfs=crfs_ess)
