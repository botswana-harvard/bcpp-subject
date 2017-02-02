import sys

from edc_constants.constants import (
    POS, YES, NEG, NO, NAIVE, DWTA, UNK)
from .models import (
    HivCareAdherence, ElisaHivResult, HivTestingHistory, HivTestReview,
    HivResultDocumentation, HivResult)

DEFAULTER = 'defaulter'
ON_ART = 'on_art'
ART_PRESCRIPTION = 'ART Prescription'


class ModelValues:

    """A class that fetches raw model values for the status
    helper class."""

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
            self.arv_evidence = obj.arv_evidence
            self.ever_taken_arv = obj.ever_taken_arv
            self.on_arv = obj.on_arv

        # ElisaHivResult
        qs = ElisaHivResult.objects.filter(
            **options).order_by('report_datetime')
        if qs:
            obj = self.get_first_positive_or_none(qs, 'hiv_result')
            if obj:
                self.elisa_hiv_result = obj.hiv_result
                self.elisa_hiv_result_date = obj.hiv_result_date
            else:
                self.elisa_hiv_result = qs.last().hiv_result
                self.elisa_hiv_result_date = qs.last().hiv_result_date

        # HivTestingHistory
        obj = HivTestingHistory.objects.filter(
            **options).order_by('report_datetime').last()
        if obj:
            self.has_tested = obj.has_tested
            self.other_record = obj.other_record
            self.self_reported_result = obj.verbal_hiv_result

        # HivTestReview
        obj = HivTestReview.objects.filter(
            **options).order_by('report_datetime').last()
        if obj:
            self.recorded_hiv_result = obj.recorded_hiv_result
            self.recorded_hiv_result_date = obj.hiv_test_date

        # HivResultDocumentation
        obj = HivResultDocumentation.objects.filter(
            **options).order_by('report_datetime').last()
        if obj:
            self.result_recorded = obj.result_recorded
            self.result_recorded_date = obj.result_date
            self.result_recorded_document = obj.result_doc_type

        # HivResult
        qs = HivResult.objects.filter(
            **options).order_by('report_datetime').last()
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


class SubjectHelper:
    """A class the determines a number of derived variables around
    HIV status and ART status.
    """

    def __init__(self, visit, model_values=None, **kwargs):
        self.documented_pos = None
        self.documented_pos_date = None
        self.final_arv_status = None
        self.final_hiv_status = None
        self.prev_result = None
        self.prev_result_date = None
        self.prev_result_known = None

        self.subject_visit = visit
        self.subject_identifier = visit.subject_identifier

        if model_values:
            for attr, value in model_values.items():
                setattr(self, attr, value)
        else:
            model_values = model_values or ModelValues(visit)
            for attr, value in model_values.__dict__.items():
                setattr(self, attr, value)

        if self.result_recorded_document == ART_PRESCRIPTION:
            self.arv_evidence = YES

        self._prepare_documented_status_and_date()
        self._prepare_final_hiv_status()
        self._prepare_final_arv_status()
        self._prepare_previous_status_date_and_awareness()

    @property
    def final_hiv_status_date(self):
        """Return the oldest POS result date or the most recent
        NEG result date.
        """
        final_hiv_status_date = self._final_hiv_status_date_if_pos
        if not final_hiv_status_date:
            final_hiv_status_date = self._final_hiv_status_date_if_neg
        return final_hiv_status_date

    @property
    def prev_results_discordant(self):
        if self.result_recorded and self.recorded_hiv_result:
            return self.result_recorded != self.recorded_hiv_result
        return False

    @property
    def best_prev_result_date(self):
        """Return best date after changing result based on ARV status.
        """
        if self.recorded_hiv_result == POS:
            best_prev_result_date = self.recorded_hiv_result_date
        elif self.result_recorded == POS:
            best_prev_result_date = self.result_recorded_date
        else:
            best_prev_result_date = None
        return best_prev_result_date

    def _prepare_previous_status_date_and_awareness(self):
        """Prepare prev_result, prev_result_date, and prev_result_known.
        * Get the POS prev_result or the NEG result.
        * If final and prev are discordant and prev_results_discordant, select the
          prev_result that equals the final result
        """
        self._update_prev_result_if(POS)
        if not self.prev_result:
            self._update_prev_result_if(NEG)
        if self.prev_results_discordant and self.final_hiv_status != self.prev_result:
            self._update_prev_result_if(self.final_hiv_status)
        if not self.prev_result:
            self._update_prev_result_if(None)
        self._previous_status_date_and_awareness_exceptions()

    def _update_prev_result_if(self, result=None):
        """Update the prev_result attributes based on the value of `result`.

        The caller is responsible for handling recorded_hiv_result
        and result_recorded being discordant.
        """
        if result and self.recorded_hiv_result == result:
            self.prev_result = result
            self.prev_result_date = self.recorded_hiv_result_date
            self.prev_result_known = YES
        elif result and self.result_recorded == result:
            self.prev_result = result
            self.prev_result_date = self.result_recorded_date
            self.prev_result_known = YES
        elif not result:
            self.prev_result = None
            self.prev_result_date = None
            self.prev_result_known = None

    def _previous_status_date_and_awareness_exceptions(self):
        """Overwrite invalid result sequence and/or derive from
        arv status if possible.
        """
        # evidence of ARV's implies POS previous result
        if (self.final_arv_status in (DEFAULTER, ON_ART)
                and (self.prev_result == NEG or not self.prev_result)):
            self.prev_result = POS
            self.prev_result_date = self.best_prev_result_date
            self.prev_result_known = YES
        # if finally NEG, a known previous result must be wrong, so flip to NEG
        if self.final_hiv_status == NEG and self.prev_result_known == YES:
            self.prev_result = NEG
            # self.debug.append('changed prev_result POS->NEG')

    def _prepare_final_arv_status(self):
        self.final_arv_status = None
        if self.final_hiv_status == POS:
            if ((not self.ever_taken_arv or self.ever_taken_arv in (NO, DWTA))
                    and (self.arv_evidence == NO or not self.arv_evidence)):
                self.final_arv_status = NAIVE
            elif ((self.ever_taken_arv == YES or self.arv_evidence == YES)
                  and self.on_arv == NO):
                self.final_arv_status = DEFAULTER
            elif ((self.arv_evidence == YES or self.ever_taken_arv == YES)
                  and self.on_arv == YES):
                self.final_arv_status = ON_ART
            elif (self.arv_evidence == YES
                  and not self.on_arv
                  and not self.ever_taken_arv):
                self.final_arv_status = ON_ART
            else:
                sys.stdout.write(
                    'Cannot determine final_arv_status for {}. '
                    'Got ever_taken_arv={}, on_arv={}, arv_evidence={}'.format(
                        self.subject_identifier,
                        self.ever_taken_arv,
                        self.on_arv,
                        self.arv_evidence))

    def _prepare_documented_status_and_date(self):
        if self.recorded_hiv_result == POS:
            self.documented_pos = YES
            self.documented_pos_date = self.recorded_hiv_result_date
        elif self.other_record == YES and self.result_recorded == POS:
            self.documented_pos = YES
            self.documented_pos_date = self.result_recorded_date
        elif self.arv_evidence == YES:
            self.documented_pos = YES
            self.documented_pos_date = None
        elif (self.recorded_hiv_result not in (POS, NEG) and
                not (self.other_record == YES and self.result_recorded == POS)):
            self.documented_pos = NO
            self.documented_pos_date = None
        else:
            self.documented_pos = NO
            self.documented_pos_date = None

    def _prepare_final_hiv_status(self):
        if self.elisa_hiv_result in (POS, NEG):
            self.final_hiv_status = self.elisa_hiv_result
        elif self.today_hiv_result in (POS, NEG):
            self.final_hiv_status = self.today_hiv_result
        elif self.documented_pos == YES:
            self.final_hiv_status = POS
        else:
            self.final_hiv_status = UNK

    @property
    def _final_hiv_status_date_if_pos(self):
        """Return oldest date if final result is POS.
        """
        final_hiv_status_date = None
        if self.final_hiv_status == POS:
            if self.prev_result_known == YES and self.prev_result == POS:
                final_hiv_status_date = self.prev_result_date
            elif self.today_hiv_result == POS:
                final_hiv_status_date = self.today_hiv_result_date
            elif self.elisa_hiv_result == POS:
                final_hiv_status_date = self.elisa_hiv_result_date
        return final_hiv_status_date

    @property
    def _final_hiv_status_date_if_neg(self):
        """Return most recent date if final result is NEG.
        """
        final_hiv_status_date = None
        if self.final_hiv_status == NEG:
            if self.elisa_hiv_result_date:
                final_hiv_status_date = self.elisa_hiv_result_date
            elif self.today_hiv_result_date:
                final_hiv_status_date = self.today_hiv_result_date
            elif self.prev_result_known == YES and self.prev_result == NEG:
                final_hiv_status_date = self.prev_result_date
        return final_hiv_status_date
