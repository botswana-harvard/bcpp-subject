from edc_visit_schedule.schedule import Schedule

from .crfs_bhs import crfs_bhs
from .requisitions import requisitions

bhs_schedule = Schedule(name='bhs_schedule', title='BHS')

bhs_schedule.add_visit(
    code='T0',
    title='Baseline Survey',
    timepoint=0,
    base_interval=0,
    requisitions=requisitions,
    crfs=crfs_bhs)
