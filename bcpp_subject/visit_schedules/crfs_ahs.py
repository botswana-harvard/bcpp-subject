from edc_map.site_mappers import site_mappers
from edc_visit_schedule.visit import Crf

from bcpp_community import is_intervention

_crfs_ahs = (
    Crf(show_order=10, model='bcpp_subject.residencymobility', required=True),
    Crf(show_order=20, model='bcpp_subject.demographics', required=True),
    Crf(show_order=30, model='bcpp_subject.education', required=True),
    Crf(show_order=40, model='bcpp_subject.hivtestinghistory', required=True),
    Crf(show_order=50, model='bcpp_subject.hivtestreview', required=True),
    Crf(show_order=60, model='bcpp_subject.hivresultdocumentation',
        required=True),
    Crf(show_order=70, model='bcpp_subject.hivtested', required=True),
    Crf(show_order=85, model='bcpp_subject.hivcareadherence', required=True),
    Crf(show_order=90, model='bcpp_subject.sexualbehaviour', required=True),
    Crf(show_order=100, model='bcpp_subject.recentpartner', required=True),
    Crf(show_order=110, model='bcpp_subject.secondpartner', required=True),
    Crf(show_order=120, model='bcpp_subject.thirdpartner', required=True),
    Crf(show_order=140, model='bcpp_subject.hivmedicalcare', required=True),
    Crf(show_order=145, model='bcpp_subject.accesstocare', required=False),
    Crf(show_order=150, model='bcpp_subject.circumcision', required=True),
    Crf(show_order=160, model='bcpp_subject.circumcised', required=True),
    Crf(show_order=170, model='bcpp_subject.uncircumcised', required=True),
    Crf(show_order=180,
        model='bcpp_subject.reproductivehealth', required=True),
    Crf(show_order=210, model='bcpp_subject.medicaldiagnoses', required=True),
    Crf(show_order=215,
        model='bcpp_subject.hypertensioncardiovascular', required=True),
    Crf(show_order=220, model='bcpp_subject.heartattack', required=True),
    Crf(show_order=230, model='bcpp_subject.cancer', required=True),
    Crf(show_order=240, model='bcpp_subject.hivrelatedillness', required=True),
    Crf(show_order=250, model='bcpp_subject.tuberculosis', required=True),
    Crf(show_order=260, model='bcpp_subject.tbsymptoms', required=True),
    Crf(show_order=270, model='bcpp_subject.qualityoflife', required=True),
    Crf(show_order=280,
        model='bcpp_subject.resourceutilization', required=True),
    Crf(show_order=290, model='bcpp_subject.outpatientcare', required=True),
    Crf(show_order=300, model='bcpp_subject.hospitaladmission', required=True),
    Crf(show_order=310,
        model='bcpp_subject.hivhealthcarecosts', required=True),
    Crf(show_order=320, model='bcpp_subject.labourmarketwages', required=True),
    Crf(show_order=330, model='bcpp_subject.hivlinkagetocare', required=True),
    Crf(show_order=340, model='bcpp_subject.hivresult', required=True),
    Crf(show_order=350, model='bcpp_subject.elisahivresult',
        required=False, additional=True),
    Crf(show_order=360, model='bcpp_subject.pimacd4',
        required=False, additional=True),
    Crf(show_order=370, model='bcpp_subject.hicenrollment',
        required=False, additional=True),
    Crf(show_order=380, model='bcpp_subject.subjectreferral', required=True),
)


# change according to intervention or not
if is_intervention(site_mappers.current_map_area):
    crfs_ahs = [crf for crf in _crfs_ahs
                if crf.model not in ['bcpp_subject.hivuntested']]
else:
    crfs_ahs = [crf for crf in _crfs_ahs
                if crf.model not in ['bcpp_subject.tbsymptoms', 'bcpp_subject.hivuntested']]
