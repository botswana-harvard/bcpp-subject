from edc_visit_schedule.constants import YEARS
from edc_visit_schedule import Schedule, Visit

from .crfs_ahs import crfs_ahs
from .requisitions import requisitions
from dateutil.relativedelta import relativedelta

ahs_schedule = Schedule(
    name='ahs_schedule',
    title='AHS',
    enrollment_model='bcpp_subject.enrollmentahs',
    disenrollment_model='bcpp_subject.disenrollmentahs',)

visit1 = Visit(
    code='T1',
    title='1st Annual Survey',
    timepoint=1,
    rbase=relativedelta(years=1),
    rlower=relativedelta(years=0),
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs_ahs)

visit2 = Visit(
    code='T2',
    title='2nd Annual Survey',
    timepoint=2,
    rbase=relativedelta(years=2),
    rlower=relativedelta(years=0),
    base_interval_unit=YEARS,
    requisitions=requisitions,
    crfs=crfs_ahs)

ahs_schedule.add_visit(visit=visit1)
ahs_schedule.add_visit(visit=visit2)

# ahs_schedule.add_visit(
#     code='T3',
#     title='3rd Annual Survey',
#     timepoint=3,
#     base_interval=3,
#     base_interval_unit=YEARS,
#     requisitions=requisitions,
#     crfs=crfs_ahs)
