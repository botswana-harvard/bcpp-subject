from edc_visit_schedule.constants import YEARS
from edc_visit_schedule.schedule import Schedule

from .crfs_ahs import crfs_ahs
from .requisitions import requisitions

ahs_schedule = Schedule(name='ahs_schedule', title='AHS')

ahs_schedule.add_visit(
    code='T1',
    title='1st Annual Survey',
    timepoint=1,
    base_interval=1,
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs_ahs)

ahs_schedule.add_visit(
    code='T2',
    title='2nd Annual Survey',
    timepoint=2,
    base_interval=2,
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs_ahs)

ahs_schedule.add_visit(
    code='T3',
    title='3rd Annual Survey',
    timepoint=3,
    base_interval=3,
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs_ahs)
