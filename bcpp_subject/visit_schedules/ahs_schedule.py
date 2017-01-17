from edc_visit_schedule.schedule import Schedule

from .crfs_ahs import crfs_ahs
from .requisitions import requisitions
from edc_visit_schedule.constants import YEARS

# schedule for existing participants
ahs_schedule = Schedule(name='ahs_schedule',)

ahs_schedule.add_visit(
    code='T1',
    title='First Annual Household Survey',
    timepoint=1,
    base_interval=1,
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs_ahs)

ahs_schedule.add_visit(
    code='T2',
    title='Second Annual Household Survey',
    timepoint=2,
    base_interval=2,
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs_ahs)

ahs_schedule.add_visit(
    code='T3',
    title='Final Annual Household Survey',
    timepoint=3,
    base_interval=3,
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs_ahs)
