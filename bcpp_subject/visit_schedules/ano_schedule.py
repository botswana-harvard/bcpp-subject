from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Visit

from .crfs_ess import crfs_ess
from .requisitions import requisitions

ano_schedule = Schedule(
    name='ano_schedule',
    title='Anonymous',
    enrollment_model='bcpp_subject.enrollmentano',
    disenrollment_model='bcpp_subject.disenrollmentano')

ano_visit = Visit(
    code='A0',
    title='Anonymous Survey',
    timepoint=0,
    base_interval=0,
    requisitions=requisitions,
    crfs=crfs_ess)

ano_schedule.add_visit(visit=ano_visit)
