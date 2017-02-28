import json
import dateutil.parser
import io
from django.apps import apps as django_apps
from bcpp_subject.models import SubjectConsent, SubjectVisit
from bcpp_subject.referral.referral import Referral
from bcpp_subject.tests.test_mixins import SubjectMixin
from django.test import TestCase
from edc_metadata.models import CrfMetadata, RequisitionMetadata
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from bcpp_subject.models.subject_requisition import SubjectRequisition
from decimal import Decimal
from django.utils import timezone
from json import JSONDecoder
from edc_constants.constants import YES

# Read existing bhs data entered by CB's

visit_gender_list = []

for subject_visit in SubjectVisit.objects.filter(visit_code='T0'):
    try:
        SubjectConsent.objects.get(subject_identifier=subject_visit.subject_identifier)
        rf_code = Referral(subject_visit).referral_code
        crf = CrfMetadata.objects.filter(
            subject_identifier=subject_visit.subject_identifier,
            visit_code='T0',
            entry_status='KEYED')
        req = RequisitionMetadata.objects.filter(
            subject_identifier=subject_visit.subject_identifier,
            visit_code='T0',
            entry_status='KEYED')
        if not (crf.count() == 0 and req.count() == 0):
            visit_gender_list.append([
                subject_visit, subject_visit.household_member.gender, rf_code])
    except SubjectConsent.DoesNotExist:
        pass
    except SubjectConsent.MultipleObjectsReturned:
        pass

# Useful methods.
class T(SubjectMixin, TestCase):
    pass
t = T()

s_id = []

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return str(obj)
    else:
        raise TypeError("Unserializable object {} of type {}".format(obj, type(obj)))


class DateTimeDecoder(json.JSONDecoder):

    def __init__(self, *args, **kargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object,
                             *args, **kargs)
    def dict_to_object(self, d):
        if '__type__' not in d:
            return d
        type = d.pop('__type__')
        try:
            dateobj = datetime(**d)
            return dateobj
        except:
            d['__type__'] = type
            return d

#  Write data to a file.

for visit, gender in visit_gender_list:
    rf_code = Referral(visit).referral_code
    fname = rf_code + '.json'
    data = {}
    for crf in site_visit_schedules.get_schedule('bhs_schedule').visit_registry['T0'].crfs:
        try:
            crf_dict = crf.model.objects.get(subject_visit=visit).__dict__
            if crf_dict.get('_state'):
                del crf_dict['_state']
            if crf_dict.get('id'):
                del crf_dict['id']
            if crf_dict.get('subject_visit_id'):
                del crf_dict['subject_visit_id']
            crf_name = crf.model_label_lower
            data[crf_name] = crf_dict
        except crf.model.DoesNotExist:
            pass
    count = 0
    for requisition in SubjectRequisition.objects.filter(subject_visit=visit):
        requisition_dict = requisition.__dict__
        if requisition_dict.get('id'):
            del requisition_dict['id']
        if requisition_dict.get('_subject_visit_cache'):
            del requisition_dict['_subject_visit_cache']
        if requisition_dict.get('requisition_identifier'):
            del requisition_dict['requisition_identifier']
        if requisition_dict.get('_state'):
            del requisition_dict['_state']
        if requisition_dict.get('subject_visit_id'):
            del requisition_dict['subject_visit_id']
        rq_name = SubjectRequisition._meta.label_lower + str(count)
        count += 1
        data[rq_name] = requisition_dict
    outfile = io.open(fname, 'w', encoding='utf8')
    str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ':'), ensure_ascii=False, default=date_handler)
    outfile.write(to_unicode(str_))


#  Read data from json files
s_id = []
rf_dict = {'POS#-PR': 'F', 'TST-CD4': 'M', 'POS#-AN': 'F', 'POS#-LO': 'F', 'SMC-UNK': 'M', 'MASA-CC': 'F', 'POS#-HI': 'M', 'UNK?-PR': 'F', 'NEG!-PR': 'F', 'SMC-NEG': 'M'}
fnames = ['POS#-PR.json', 'TST-CD4.json', 'POS#-AN.json', 'POS#-LO.json', 'SMC-UNK.json', 'MASA-CC.json', 'POS#-HI.json', 'UNK?-PR.json', 'NEG!-PR.json', 'SMC-NEG.json']
path_name = '/Users/django/source/bcpp/'
for fname in fnames:
    file = path_name + fname
    with open(file) as data_file:
        data_loaded = json.load(data_file, cls=DateTimeDecoder)
    subject_visit = None
    print('-------------------------------------------------------------------')
    if rf_dict.get(fname[:-5]) == 'F':
        subject_visit = t.make_subject_visit_for_consented_subject_female('T0')
        subject_visit = SubjectVisit.objects.get(id=subject_visit.id)
    elif rf_dict.get(fname[:-5]) == 'M':
        subject_visit = t.make_subject_visit_for_consented_subject_male('T0')
        subject_visit = SubjectVisit.objects.get(id=subject_visit.id)
    print(rf_dict.get(fname[:-5]), fname[:-5], 'starting')
    print(subject_visit.subject_identifier)
    for label_lower, model_dict in data_loaded.items():
        if subject_visit:
            s_id.append(subject_visit.subject_identifier)
            if label_lower[:-1] == 'bcpp_subject.subjectrequisition':
                label_lower = 'bcpp_subject.subjectrequisition'
                model_dict.update(received=False)
                model_dict.update(processed=False)
                model_dict.update(packed=False)
                model_dict.update(shipped=False)
                if model_dict.get('requisition_identifier'):
                    del model_dict['requisition_identifier']
                if not model_dict.get('reason_not_drawn') and model_dict.get('is_drawn') == YES:
                    model_dict.update(reason_not_drawn='refused')
            app_label, model_name = label_lower.split('.')
            print(label_lower)
            model = django_apps.get_model(app_label, model_name)
            my_datetime = timezone.make_aware(timezone.datetime(2013, 10, 18, 16, 41, 1, 173694), timezone.get_current_timezone())
            if label_lower == 'bcpp_subject.sexualbehaviour':
                model_dict.update(first_sex_partner_age=24)
            if model_dict.get('report_datetime'):
                model_dict.update(report_datetime=my_datetime)
            if model_dict.get('cd4_value'):
                cd4_value = Decimal(model_dict.get('cd4_value'))
                model_dict.update(cd4_value=cd4_value)
            if model_dict.get('created'):
                model_dict.update(created=my_datetime)
            if model_dict.get('modified'):
                model_dict.update(modified=my_datetime)
            if model_dict.get('_state'):
                del crf_dict['_state']
            if model_dict.get('id'):
                del model_dict['id']
            if model_dict.get('_subject_visit_cache'):
                del model_dict['_subject_visit_cache']
            if model_dict.get('requisition_identifier'):
                del model_dict['requisition_identifier']
            model_dict.update(subject_visit_id=subject_visit.id)
            obj = model(**model_dict)
            obj.save()
    print(fname, 'Done')
    print('-------------------------------------------------------------------')

for og_subject_visit, gender in visit_gender_list:
    new_scenario_number = 12
    while new_scenario_number < 0:
        if gender == 'F':
            clone_subject_visit = t.make_subject_visit_for_consented_subject_female('T0')
            clone_subject_visit = SubjectVisit.objects.get(id=clone_subject_visit.id)
        elif gender == 'M':
            clone_subject_visit = t.make_subject_visit_for_consented_subject_male('T0')
            clone_subject_visit = SubjectVisit.objects.get(id=clone_subject_visit.id)
        s_id.append(clone_subject_visit.subject_identifier)
        for crf in site_visit_schedules.get_schedule('bhs_schedule').visit_registry['T0'].crfs:
            try:
                crf_dict = crf.model.objects.get(subject_visit=og_subject_visit).__dict__
                if crf_dict.get('_state'):
                    del crf_dict['_state']
                if crf_dict.get('id'):
                    del crf_dict['id']
                crf_dict.update(subject_visit_id=clone_subject_visit.id)
                crf.model.objects.create(**crf_dict)
            except crf.model.DoesNotExist:
                pass
        for requisition in site_visit_schedules.get_schedule('bhs_schedule').visit_registry['T0'].requisitions:
            for requisition_dict in requisition.model.objects.filter(subject_visit=og_subject_visit):
                try:
                    requisition_dict = requisition_dict.__dict__
                    if requisition_dict.get('id'):
                        del requisition_dict['id']
                    if requisition_dict.get('_subject_visit_cache'):
                        del requisition_dict['_subject_visit_cache']
                    if requisition_dict.get('requisition_identifier'):
                        del requisition_dict['requisition_identifier']
                    if requisition_dict.get('_state'):
                        del requisition_dict['_state']
                    requisition_dict.update(subject_visit_id=clone_subject_visit.id)
                    requisition.model.objects.create(**requisition_dict)
                except requisition.model.MultipleObjectsReturned:
                    pass
        new_scenario_number -= 1
