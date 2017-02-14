from edc_constants.constants import POS, NOT_APPLICABLE

from ..models import (
    HivCareAdherence, ElisaHivResult, HivTestingHistory, HivTestReview,
    HivResultDocumentation, HivResult)


class ModelValues:

    """A class that fetches raw model values for the status
    helper class.
    """

    def __init__(self, visit):
        self.arv_evidence = None
        self.elisa_hiv_result = None
        self.elisa_hiv_result_date = None
        self.ever_taken_arv = None
        self.has_tested = None
        self.on_arv = None
        self.other_record = None
        self.recorded_hiv_result = None
        self.recorded_hiv_result_date = None
        self.result_recorded = None
        self.result_recorded_document = None
        self.self_reported_result = None
        self.today_hiv_result = None
        self.today_hiv_result_date = None

        options = dict(
            subject_visit__subject_identifier=visit.subject_identifier,
            subject_visit__report_datetime__lte=visit.report_datetime)

        # HivCareAdherence
        obj = HivCareAdherence.objects.filter(
            **options).order_by('report_datetime').last()
        if obj:
            self.arv_evidence = None if obj.arv_evidence == NOT_APPLICABLE else obj.arv_evidence
            self.ever_taken_arv = obj.ever_taken_arv
            self.on_arv = None if self.on_arv == NOT_APPLICABLE else obj.on_arv

        # ElisaHivResult
        qs = ElisaHivResult.objects.filter(
            **options).order_by('report_datetime')
        if qs:
            obj = self.get_first_positive_or_none(qs, 'hiv_result')
            if obj:
                self.elisa_hiv_result = obj.hiv_result
                self.elisa_hiv_result_date = obj.hiv_result_datetime
            else:
                self.elisa_hiv_result = qs.last().hiv_result
                self.elisa_hiv_result_date = qs.last().hiv_result_datetime

        # HivTestingHistory
        qs = HivTestingHistory.objects.filter(
            **options).order_by('report_datetime')
        if qs:
            obj = self.get_first_positive_or_none(qs, 'verbal_hiv_result')
            if obj:
                self.has_tested = obj.has_tested
                self.other_record = obj.other_record
                self.self_reported_result = obj.verbal_hiv_result
            else:
                self.has_tested = qs.last().has_tested
                self.other_record = qs.last().other_record
                self.self_reported_result = qs.last().verbal_hiv_result

        # HivTestReview
        qs = HivTestReview.objects.filter(
            **options).order_by('report_datetime')
        if qs:
            obj = self.get_first_positive_or_none(qs, 'recorded_hiv_result')
            if obj:
                self.recorded_hiv_result = obj.recorded_hiv_result
                self.recorded_hiv_result_date = obj.hiv_test_date
            else:
                self.recorded_hiv_result = qs.last().recorded_hiv_result
                self.recorded_hiv_result_date = qs.last().hiv_test_date

        # HivResultDocumentation
        qs = HivResultDocumentation.objects.filter(
            **options).order_by('report_datetime')
        if qs:
            obj = self.get_first_positive_or_none(qs, 'result_recorded')
            if obj:
                self.result_recorded = obj.result_recorded
                self.result_recorded_date = obj.result_date
                self.result_recorded_document = obj.result_doc_type
            else:
                self.result_recorded = qs.last().result_recorded
                self.result_recorded_date = qs.last().result_date
                self.result_recorded_document = qs.last().result_doc_type

        # HivResult performed, not declined
        qs = HivResult.objects.filter(
            hiv_result_datetime__isnull=False,
            **options).order_by('report_datetime')
        if qs:
            obj = self.get_first_positive_or_none(qs, 'hiv_result')
            if obj:
                self.today_hiv_result = obj.hiv_result
                self.today_hiv_result_date = obj.hiv_result_datetime.date()
            else:
                self.today_hiv_result = qs.last().hiv_result
                self.today_hiv_result_date = (
                    qs.last().hiv_result_datetime.date())

    def get_first_positive_or_none(self, qs, field_name):
        """Returns the first model instance that is POS or None.
        """
        for obj in qs:
            if getattr(obj, field_name) == POS:
                return obj
        return None
