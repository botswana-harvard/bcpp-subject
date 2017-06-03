from edc_visit_schedule.schedule import Schedule

from .crfs_ess import crfs_ess
from .requisitions import requisitions

ano_schedule = Schedule(
    name='ano_schedule',
    title='Anonymous',
    enrollment_model='bcpp_subject.enrollmentano',
    disenrollment_model='bcpp_subject.disenrollmentano')

ano_schedule.add_visit(
    code='A0',
    title='Anonymous Survey',
    timepoint=0,
    base_interval=0,
    requisitions=requisitions,
    crfs=crfs_ess)
