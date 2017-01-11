from edc_visit_schedule.schedule import Schedule

from .crfs_ahs import crfs_ahs
from .crfs_bhs import crfs_bhs
from .requisitions import requisitions

# schedule for existing participants
annual_schedule = Schedule(name='annual_schedule',)

annual_schedule.add_visit(
    code='T0',
    title='Baseline Household Survey',
    timepoint=0,
    base_interval=0,
    requisitions=requisitions,
    crfs=crfs_bhs)

annual_schedule.add_visit(
    code='T1',
    title='First Annual Household Survey',
    timepoint=1,
    base_interval=1,
    requisitions=requisitions,
    crfs=crfs_ahs)

annual_schedule.add_visit(
    code='T2',
    title='Second Annual Household Survey',
    timepoint=2,
    base_interval=2,
    requisitions=requisitions,
    crfs=crfs_ahs)

annual_schedule.add_visit(
    code='T3',
    title='Final Annual Household Survey',
    timepoint=3,
    base_interval=3,
    requisitions=requisitions,
    crfs=crfs_ahs)
