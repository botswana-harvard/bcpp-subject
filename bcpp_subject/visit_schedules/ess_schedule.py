from edc_visit_schedule.schedule import Schedule

from .crfs_ess import crfs_ess
from .requisitions import requisitions

# schedule for new participants
ess_schedule = Schedule(name='ess_schedule', title='ESS')

ess_schedule.add_visit(
    code='E0',
    title='End-of-study Household Survey',
    timepoint=0,
    base_interval=0,
    requisitions=requisitions,
    crfs=crfs_ess)
