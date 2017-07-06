from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Visit

from .crfs_ess import crfs_ess
from .requisitions import requisitions

# schedule for new participants
ess_schedule = Schedule(
    name='ess_schedule',
    title='ESS',
    enrollment_model='bcpp_subject.enrollmentess',
    disenrollment_model='bcpp_subject.disenrollmentess')

ess_visit = Visit(
    code='E0',
    title='End-of-study Household Survey',
    timepoint=0,
    base_interval=0,
    requisitions=requisitions,
    crfs=crfs_ess)

ess_schedule.add_visit(visit=ess_visit)
