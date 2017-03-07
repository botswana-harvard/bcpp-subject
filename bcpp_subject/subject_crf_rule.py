from edc_rule_groups.crf_rule import CrfRule


class BhsCrfRule(CrfRule):

    visit_schedule_name = 'visit_schedule_bhs'
    schedule_name = 'bhs_schedule'

    def __init__(self, target_models, visit_codes=None, **kwargs):
        super().__init__(target_models, visit_codes, **kwargs)
        self.visit_codes = visit_codes


class AhsCrfRule(CrfRule):

    def __init__(self, target_models, visit_codes=None, **kwargs):
        super().__init__(target_models, visit_codes, **kwargs)
        self.visit_codes = visit_codes

    visit_schedule_name = 'visit_schedule_ahs'
    schedule_name = 'ahs_schedule'


class EssCrfRule(CrfRule):

    visit_schedule_name = 'visit_schedule_ess'
    schedule_name = 'ess_schedule'

    def __init__(self, target_models, visit_codes=None, **kwargs):
        super().__init__(target_models, visit_codes, **kwargs)
        self.visit_codes = visit_codes


class CommonCrfRule(CrfRule):

    def runif(self, visit, **kwargs):
        return True
