from dateutil.relativedelta import relativedelta

from edc_visit_schedule.constants import YEARS
from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Visit

from .crfs_ahs import crfs_ahs
from .requisitions import requisitions

ahs_schedule = Schedule(
    name='ahs_schedule',
    title='AHS',
    enrollment_model='bcpp_subject.enrollmentahs',
    disenrollment_model='bcpp_subject.disenrollmentahs',)

ahs_visit1 = Visit(
    code='T1',
    title='1st Annual Survey',
    timepoint=1,
    rbase=relativedelta(years=1),
    rlower=relativedelta(years=0),
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs_ahs)

ahs_visit2 = Visit(
    code='T2',
    title='2nd Annual Survey',
    timepoint=2,
    rbase=relativedelta(years=2),
    rlower=relativedelta(years=0),
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs_ahs)

# ahs_schedule.add_visit(
#     code='T3',
#     title='3rd Annual Survey',
#     timepoint=3,
#     base_interval=3,
#     base_interval_unit=YEARS,
#     requisitions=requisitions,
#     crfs=crfs_ahs)

ahs_schedule.add_visit(visit=ahs_visit1)
ahs_schedule.add_visit(visit=ahs_visit2)
