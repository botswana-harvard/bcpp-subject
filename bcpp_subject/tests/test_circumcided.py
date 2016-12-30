# from django.test import TestCase
# from edc_visit_schedule.constants import YEARS
# from dateutil.relativedelta import relativedelta
# from datetime import date
# from models import Circumcised
# 
# 
# class CircumcisedModelTest(TestCase):
#     """Setup data with all required fields for circumcised"""
# #     def setUp(self):
# #         self.data = {
# #             circ_date: date.today(),
# #             when_circ: 14,
# #             age_unit_circ: "14 years",
# #             where_circ: "hospital",
# #             where_circ_other:None,
# #             why_circ:"medical-reason",
# #             why_circ_other:None,
# 
# 
#     def test_if_circumcised == YES and not self.health_benefits_smc(self):
#         """Test to verify if the participant answered yes to circumcision and knows abt the benefits"""
#         self.data[' where_circ'] = "hospital"
#         self.assertFalse('if {}, what are the benefits of male circumcision?.')
# 
#     def test_if_not_circumcised == NO and not self.health_benefits_smc(self):
#         """Test to verify if the participant answered yes to circumcision and knows abt the benefits"""
#         self.data[' where_circ_other'] = None
#         self.assertFalse()
