from edc_visit_schedule.schedule import Schedule
from edc_visit_schedule.visit import Visit

from .crfs_bhs import crfs_bhs
from .requisitions import requisitions

bhs_schedule = Schedule(
    name='bhs_schedule',
    title='BHS',
    enrollment_model='bcpp_subject.enrollmentbhs',
    disenrollment_model='bcpp_subject.disenrollmentbhs',)

bhs_visit = Visit(
    code='T0',
    title='Baseline Survey',
    timepoint=0,
    base_interval=0,
    requisitions=requisitions,
    crfs=crfs_bhs)

bhs_schedule.add_visit(visit=bhs_visit)
