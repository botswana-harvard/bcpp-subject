from model_mommy import mommy
from datetime import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker

from edc_appointment.constants import IN_PROGRESS_APPT
from edc_constants.constants import YES, NO, NEG, OTHER, NOT_APPLICABLE

from household.constants import ELIGIBLE_REPRESENTATIVE_PRESENT
from household.models import Household, HouseholdStructure
from household.tests import HouseholdTestHelper
from member.constants import HEAD_OF_HOUSEHOLD
from member.models import EnrollmentChecklist, HouseholdMember
from plot.constants import ACCESSIBLE, RESIDENTIAL_HABITABLE
from plot.models import PlotLog
from plot.mommy_recipes import GpsProvider

from ..constants import T0
from ..models import Appointment
from ..models.list_models import Diagnoses, CircumcisionBenefits

fake = Faker()
fake.add_provider(GpsProvider)


class TestDummyData:

    household_helper = HouseholdTestHelper()

    def subject_visit(self, gender, omang):
        report_datetime = datetime.today()

        #  Create plot
        plot = mommy.make_recipe(
            'plot.plot',
            plot_identifier=None,
            report_datetime=report_datetime)

        #  Create log entry
        plot_log = PlotLog.objects.get(plot=plot)

        mommy.make_recipe(
            'plot.plotlogentry',
            plot_log=plot_log,
            log_status=ACCESSIBLE,
            report_datetime=report_datetime)

        #  Confirm plot

        plot.gps_confirmed_latitude = fake.confirmed_latitude()
        plot.gps_confirmed_longitude = fake.confirmed_longitude()
        plot.household_count = 1
        plot.status = RESIDENTIAL_HABITABLE
        plot.time_of_day = 'mornings'
        plot.time_of_week = 'weekdays'
        plot.save()
        household = Household.objects.get(plot=plot)

        survey_schedule = HouseholdMixin.get_survey_schedule(0)
        household_structure = HouseholdStructure.objects.get(
            household=household,
            survey_schedule=survey_schedule.field_value)

        #  Add today's log entry
        mommy.make_recipe(
            'household.householdlogentry',
            report_datetime=report_datetime,
            household_log=household_structure.householdlog,
            household_status=ELIGIBLE_REPRESENTATIVE_PRESENT)

        #  Add representative eligibility
        mommy.make_recipe(
            'member.representativeeligibility',
            report_datetime=report_datetime,
            household_structure=household_structure)

        first_name = fake.first_name()
        last_name = fake.last_name()

        household_member = mommy.make_recipe(
            'member.householdmember',
            household_structure=household_structure,
            report_datetime=report_datetime,
            first_name=first_name,
            initials=first_name[0] + last_name[0],
            gender=gender,
            relation=HEAD_OF_HOUSEHOLD)

        mommy.make_recipe(
            'member.householdheadeligibility',
            report_datetime=report_datetime,
            household_member=household_member)

        dob = (
            report_datetime - relativedelta(years=household_member.age_in_years)).date()
        mommy.make_recipe(
            'member.enrollmentchecklist',
            household_member=household_member,
            report_datetime=report_datetime,
            initials=household_member.initials,
            gender=household_member.gender,
            dob=dob)

        enrollment_checklist = EnrollmentChecklist.objects.get(
            household_member=household_member)

        household_member = HouseholdMember.objects.get(pk=household_member.pk)

        mommy.make_recipe(
            'bcpp_subject.subjectconsent',
            survey_schedule=household_member.survey_schedule_object.field_value,
            first_name=household_member.first_name,
            last_name=last_name,
            dob=enrollment_checklist.dob,
            consent_datetime=report_datetime,
            gender=enrollment_checklist.gender,
            initials=enrollment_checklist.initials,
            is_literate=enrollment_checklist.literacy,
            witness_name=None,
            legal_marriage=enrollment_checklist.legal_marriage,
            marriage_certificate=enrollment_checklist.marriage_certificate,
            guardian_name=None,
            identity=omang,
            confirm_identity=omang,
            household_member=household_member)

        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=T0)
        appointment.appt_status = IN_PROGRESS_APPT
        appointment.save()

        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            subject_identifier=household_member.subject_identifier,
            appointment=appointment,
            report_datetime=report_datetime)

    def smc_unk(self, subject_visit):
        """ Create an smc-unk subject scenario."""
        mommy.make_recipe(
            'bcpp_subject.subjectlocator',
            subject_identifier=subject_visit.subject_identifier,
            report_datetime=subject_visit.report_datetime)

        mommy.make_recipe(
            'bcpp_subject.residencymobility',
            subject_visit=subject_visit,
            report_datetime=subject_visit.report_datetime,
            length_residence='1 to 5 years',
            permanent_resident=YES,
            intend_residency=NO,
            nights_away='1-3 months',
            cattle_postlands='Other community',
            cattle_postlands_other='SEROWE, BOBONONG')

        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            report_datetime=subject_visit.report_datetime,
            has_tested=YES,
            when_hiv_test='more than 12 months ago',
            has_record=NO,
            verbal_hiv_result=NEG,
            subject_visit=subject_visit)

        mommy.make_recipe(
            'bcpp_subject.hivtested',
            report_datetime=subject_visit.report_datetime,
            num_hiv_tests=1,
            where_hiv_test='Tebelopele VCT center',
            why_hiv_test=OTHER,
            hiv_pills=YES,
            arvs_hiv_test=YES,
            subject_visit=subject_visit)

        mommy.make_recipe(
            'bcpp_subject.sexualbehaviour',
            report_datetime=subject_visit.report_datetime,
            ever_sex=YES,
            lifetime_sex_partners=10,
            last_year_partners=0,
            first_sex=20,
            condom=YES,
            alcohol_sex='Neither of us',
            subject_visit=subject_visit)

        health_benefits_smc = CircumcisionBenefits.objects.get(
            name='Improved hygiene')

        mommy.make_recipe(
            'bcpp_subject.circumcision',
            health_benefits_smc=[health_benefits_smc.id],
            circumcised=NO,
            circumcised_datetime=None,
            report_datetime=subject_visit.report_datetime,
            subject_visit=subject_visit)

        mommy.make_recipe(
            'bcpp_subject.uncircumcised',
            circumcised='Not Sure',
            health_benefits_smc=[health_benefits_smc.id],
            reason_circ=OTHER,
            reason_circ_other='THINK ITS NOT NECESSARY',
            future_circ=YES,
            future_reasons_smc='not_sure',
            service_facilities=YES,
            aware_free='Radio',
            report_datetime=subject_visit.report_datetime,
            subject_visit=subject_visit)

        diagnoses = Diagnoses.objects.get(name='Other serious infection')

        mommy.make_recipe(
            'bcpp_subject.medicaldiagnoses',
            report_datetime=subject_visit.report_datetime,
            subject_visit=subject_visit,
            diagnoses=[diagnoses.id],
            heart_attack_record=None,
            cancer_record=None,
            tb_record=None)

        mommy.make_recipe(
            'bcpp_subject.substanceuse',
            report_datetime=subject_visit.report_datetime,
            subject_visit=subject_visit,
            alcohol='Never',
            smoke=NO)

        mommy.make_recipe(
            'bcpp_subject.stigma',
            report_datetime=subject_visit.report_datetime,
            subject_visit=subject_visit,
            anticipate_stigma=None,
            enacted_shame_stigma=None,
            saliva_stigma=None,
            teacher_stigma=None,
            children_stigma=None)

        mommy.make_recipe(
            'bcpp_subject.hivresult',
            report_datetime=subject_visit.report_datetime,
            subject_visit=subject_visit,
            hiv_result='Not performed',
            hiv_result_datetime=None,
            blood_draw_type=None,
            insufficient_vol=None,
            why_not_tested=None)

        mommy.make_recipe(
            'bcpp_subject.subjectreferral',
            report_datetime=subject_visit.report_datetime,
            subject_visit=subject_visit,
            subject_referred=NO,
            scheduled_appt_date=None,
            referral_appt_comment=NOT_APPLICABLE,
            comment=None)
