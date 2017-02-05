import sys

from edc_constants.constants import (
    POS, YES, NEG, NO, NAIVE, DWTA, UNK)

from .model_values import ModelValues
from .constants import ART_PRESCRIPTION, DEFAULTER, ON_ART


class Raw:

    def __init__(self, model_values):
        for attr, value in model_values.items():
            if not hasattr(self, attr):
                setattr(self, attr, value)


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
        self.newly_diagnosed = None

        self.subject_visit = visit
        self.subject_identifier = visit.subject_identifier

        self.raw = Raw(model_values or ModelValues(visit).__dict__)

        if self.raw.result_recorded_document == ART_PRESCRIPTION:
            self.raw.arv_evidence = YES

        self._prepare_documented_status_and_date()
        self._prepare_final_hiv_status()
        self._prepare_final_arv_status()
        self._prepare_previous_status_date_and_awareness()
        self.newly_diagnosed = (
            not self.prev_result and self.prev_result_known != YES)
        self.known_positive = (
            self.prev_result == POS and self.prev_result_known == YES)

    @property
    def final_hiv_status_date(self):
        """Returns the oldest POS result date or the most recent
        NEG result date.
        """
        final_hiv_status_date = self._final_hiv_status_date_if_pos
        if not final_hiv_status_date:
            final_hiv_status_date = self._final_hiv_status_date_if_neg
        return final_hiv_status_date

    @property
    def prev_results_discordant(self):
        if self.raw.result_recorded and self.raw.recorded_hiv_result:
            return self.raw.result_recorded != self.raw.recorded_hiv_result
        return False

    @property
    def best_prev_result_date(self):
        """Returns best date after changing result based on ARV status.
        """
        if self.raw.recorded_hiv_result == POS:
            best_prev_result_date = self.raw.recorded_hiv_result_date
        elif self.raw.result_recorded == POS:
            best_prev_result_date = self.raw.result_recorded_date
        else:
            best_prev_result_date = None
        return best_prev_result_date

    def _prepare_previous_status_date_and_awareness(self):
        """Prepares prev_result, prev_result_date, and prev_result_known.

        * Get the POS prev_result or the NEG result.
        * If final and prev are discordant and prev_results_discordant,
          select the prev_result that equals the final result
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
        """Updates the prev_result attributes based on the value of `result`.

        The caller is responsible for handling recorded_hiv_result
        and result_recorded being discordant.
        """
        if result and self.raw.recorded_hiv_result == result:
            self.prev_result = result
            self.prev_result_date = self.raw.recorded_hiv_result_date
            self.prev_result_known = YES
        elif result and self.raw.result_recorded == result:
            self.prev_result = result
            self.prev_result_date = self.raw.result_recorded_date
            self.prev_result_known = YES
        elif not result:
            self.prev_result = None
            self.prev_result_date = None
            self.prev_result_known = None

    def _previous_status_date_and_awareness_exceptions(self):
        """Overwrites invalid result sequence and/or derives from
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
            if ((not self.raw.ever_taken_arv or self.raw.ever_taken_arv in (NO, DWTA))
                    and (self.raw.arv_evidence == NO or not self.raw.arv_evidence)):
                self.final_arv_status = NAIVE
            elif ((self.raw.ever_taken_arv == YES or self.raw.arv_evidence == YES)
                  and self.raw.on_arv == NO):
                self.final_arv_status = DEFAULTER
            elif ((self.raw.arv_evidence == YES or self.raw.ever_taken_arv == YES)
                  and self.raw.on_arv == YES):
                self.final_arv_status = ON_ART
            elif (self.raw.arv_evidence == YES
                  and not self.raw.on_arv
                  and not self.raw.ever_taken_arv):
                self.final_arv_status = ON_ART
            else:
                sys.stdout.write(
                    'Cannot determine final_arv_status for {}. '
                    'Got ever_taken_arv={}, on_arv={}, arv_evidence={}'.format(
                        self.subject_identifier,
                        self.raw.ever_taken_arv,
                        self.raw.on_arv,
                        self.raw.arv_evidence))

    def _prepare_documented_status_and_date(self):
        if self.raw.recorded_hiv_result == POS:
            self.documented_pos = YES
            self.documented_pos_date = self.raw.recorded_hiv_result_date
        elif self.raw.other_record == YES and self.raw.result_recorded == POS:
            self.documented_pos = YES
            self.documented_pos_date = self.raw.result_recorded_date
        elif self.raw.arv_evidence == YES:
            self.documented_pos = YES
            self.documented_pos_date = None
        elif (self.raw.recorded_hiv_result not in (POS, NEG) and
                not (self.raw.other_record == YES and self.raw.result_recorded == POS)):
            self.documented_pos = NO
            self.documented_pos_date = None
        else:
            self.documented_pos = NO
            self.documented_pos_date = None

    def _prepare_final_hiv_status(self):
        if self.raw.elisa_hiv_result in (POS, NEG):
            self.final_hiv_status = self.raw.elisa_hiv_result
        elif self.raw.today_hiv_result in (POS, NEG):
            self.final_hiv_status = self.raw.today_hiv_result
        elif self.documented_pos == YES:
            self.final_hiv_status = POS
        else:
            self.final_hiv_status = UNK

    @property
    def _final_hiv_status_date_if_pos(self):
        """Returns oldest date if final result is POS.
        """
        final_hiv_status_date = None
        if self.final_hiv_status == POS:
            if self.prev_result_known == YES and self.prev_result == POS:
                final_hiv_status_date = self.prev_result_date
            elif self.raw.today_hiv_result == POS:
                final_hiv_status_date = self.raw.today_hiv_result_date
            elif self.raw.elisa_hiv_result == POS:
                final_hiv_status_date = self.raw.elisa_hiv_result_date
        return final_hiv_status_date

    @property
    def _final_hiv_status_date_if_neg(self):
        """Returns most recent date if final result is NEG.
        """
        final_hiv_status_date = None
        if self.final_hiv_status == NEG:
            if self.raw.elisa_hiv_result_date:
                final_hiv_status_date = self.raw.elisa_hiv_result_date
            elif self.raw.today_hiv_result_date:
                final_hiv_status_date = self.raw.today_hiv_result_date
            elif self.prev_result_known == YES and self.prev_result == NEG:
                final_hiv_status_date = self.prev_result_date
        return final_hiv_status_date
