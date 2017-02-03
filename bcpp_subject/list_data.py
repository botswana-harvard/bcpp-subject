from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from edc_constants.constants import (
    NOT_APPLICABLE, OTHER, DWTA, NONE, DONT_KNOW)


list_data = {
    'bcpp_subject.circumcisionbenefits': [
        ('Improved hygiene ', 'Improved hygiene '),
        ('Reduced risk of HIV ', 'Reduced risk of HIV '),
        ('Reduced risk of other sexually transmitted diseases',
         'Reduced risk of other sexually transmitted diseases'),
        ('Reduced risk of cancer', 'Reduced risk of cancer'),
        (OTHER, ' Other'),
        ('I am not sure', 'I am not sure'),
        (DWTA, "Don't want to answer")],
    'bcpp_subject.diagnoses': [
        ('Heart Disease', 'Heart Disease or Stroke'),
        ('Cancer', 'Cancer'),
        ('tb', 'Tubercolosis'),
        (OTHER, ' Other serious infection'),
        (NONE, ' None'),
        ('sti', 'STI (Sexually Transmitted Infection)')],
    'bcpp_subject.ethnicgroups': [
        ('Babirwa', 'Babirwa'),
        ('Bahambukushu', 'Bahambukushu'),
        ('Baherero', 'Baherero'),
        ('Bahurutshe', 'Bahurutshe'),
        ('Bakalaka', 'Bakalaka'),
        ('Bakgatla', 'Bakgatla'),
        ('Bakwena', 'Bakwena'),
        ('Balete', 'Balete'),
        ('Bangwaketse', 'Bangwaketse'),
        ('Bangwato', 'Bangwato'),
        ('Bakgalagadi', 'Bakgalagadi'),
        ('Basarwa', 'Basarwa'),
        ('Basobea', 'Basobea'),
        ('Batawana', 'Batawana'),
        ('Batlokwa', 'Batlokwa'),
        ('Batswapong', 'Batswapong'),
        ('White African', 'White African'),
        ('Indian African', 'Indian African'),
        ('Asian', 'Asian'),
        ('Other, specify', 'Other, specify'),
        (DWTA, 'dont want to answer'),
        ('Bazezuri/Shona', 'Bazezuri')],
    'bcpp_subject.familyplanning': [
        ('Condoms, consistent use (male or female)',
         'Condoms, consistent use (male or female)'),
        ('Injectable contraceptive', 'Injectable contraceptive'),
        ('Oral contraceptive', 'Oral contraceptive'),
        ('IUD', 'IUD'),
        ('Diaphragm or cervical cap', 'Diaphragm or cervical cap'),
        ('Rhythm or menstrual cycle timing',
         'Rhythm or menstrual cycle timing'),
        ('Withdrawal', 'Withdrawal'),
        (OTHER, ' OTHER, specify'),
        (DWTA, " Don't want to answer"),
        (NOT_APPLICABLE, ' NOT APPLICABLE'),
        ('Condoms, in-consistent use (male or female)',
         'Condoms, in-consistent use (male or female)')],
    'bcpp_subject.medicationtaken': [
        ("bisoprolol", "Bisoprolol"),
        ("carvedilol", "Carvedilol"),
        ("propranolol", "Propranolol"),
        ("atenolol", "Atenolol"),
        ("enalapril", "Enalapril"),
        ("captopril", "Captopril"),
        ("co_micardis", "Co-Micardis"),
        ("spirinolactone", "Spirinolactone "),
        ("hydrochlrothiazide", "Hydrochlrothiazide "),
        ("nifedipine", "Nifedipine"),
        ("amlodipine", "Amlodipine"),
        ("furosemide", "Furosemide"),
        ("doxazosin", "Doxazosin"),
        ("hydralazine", "Hydralazine"),
        ("not_applicable", "Not Applicable"),
        ("OTHER", "Other")],
    'bcpp_subject.medicationgiven': [
        ("bisoprolol", "Bisoprolol"),
        ("carvedilol", "Carvedilol"),
        ("propranolol", "Propranolol"),
        ("atenolol", "Atenolol"),
        ("enalapril", "Enalapril"),
        ("captopril", "Captopril"),
        ("co_micardis", "Co-Micardis"),
        ("spirinolactone", "Spirinolactone "),
        ("hydrochlrothiazide", "Hydrochlrothiazide "),
        ("nifedipine", "Nifedipine"),
        ("amlodipine", "Amlodipine"),
        ("furosemide", "Furosemide"),
        ("doxazosin", "Doxazosin"),
        ("hydralazine", "Hydralazine"),
        ("not_applicable", "Not Applicable"),
        (OTHER, " OTHER")],
    'bcpp_subject.heartdisease': [
        ('Myocardial infarction (heart attack)',
         'Myocardial infarction (heart attack)'),
        ('Congestive cardiac failure', 'Congestive cardiac failure'),
        ('Stroke (cerebrovascular accident, CVA)',
         'Stroke (cerebrovascular accident, CVA)'),
        (OTHER, ' OTHER, specify'),
        (DWTA, " Don't want to answer")],
    'bcpp_subject.livewith': [
        ('Partner or spouse', 'Partner or spouse'),
        ('Siblings', 'Siblings'),
        ('Alone', 'Alone'),
        ('Extended family', 'Extended family'),
        (OTHER, ' Other'),
        (DWTA, " Don't want to answer")],
    'bcpp_subject.medicalcareaccess': [
        ('Traditional, faith, or religious healer/doctor',
         'Traditional, faith, or religious healer/doctor'),
        ('Pharmacy', 'Pharmacy'),
        ('Public or government health facility or clinic',
         'Public or government health facility or clinic'),
        ('Private health facility or clinic',
         'Private health facility or clinic'),
        ('Community health worker', 'Community health worker'),
        (OTHER, ' OTHER, specify'),
        (DWTA, " Don't want to answer")],
    'bcpp_subject.neighbourhoodproblems': [
        ('Water', 'Water'),
        ('Sewer (sanitation)', 'Sewer (sanitation)'),
        ('Housing', 'Housing'),
        ('Roads', 'Roads'),
        ('Malaria', 'Malaria'),
        ('HIV/AIDS', 'HIV/AIDS'),
        ('Schools', 'Schools'),
        ('Unemployment', 'Unemployment'),
        (OTHER, ' OTHER, specify'),
        (DWTA, " Don't want to answer")],
    'bcpp_subject.partnerresidency': [
        ('in this community', 'In this community'),
        ('outside community', 'Outside community'),
        ('farm within', 'Farm within this community'),
        ('farm outside this community', 'Farm outside this community'),
        ('cattelepost within', 'Cattle post within this community'),
        ('cattlepost outside', 'Cattle post outside this community')],
    'bcpp_subject.religion': [
        ('anglican', 'Anglican'),
        ('apostolic', 'Apostolic'),
        ('baptist', 'Baptist'),
        ('catholic', 'Catholic'),
        ('evangelical', 'Evangelical'),
        ('methodist', 'Methodist'),
        ('pentecostal', 'Pentecostal'),
        ('traditionalist', 'Traditionalist'),
        ('zcc', 'ZCC'),
        ('muslim', 'Islam'),
        ('hindu', 'HInduism'),
        ('buddhist', 'Buddhism'),
        (OTHER, ' OTHER, specify'),
        ('No affiliation', 'no_affiliation')],
    'bcpp_subject.stiillnesses': [
        ('wasting',
         'Severe weight loss (wasting) - more than 10% of body weight'),
        ('diarrhoea', 'Unexplained diarrhoea for one month'),
        ('yeast_infection', 'Yeast infection of mouth or oesophagus'),
        ('pneumonia', 'Severe pneumonia or meningitis or sepsis'),
        ('PCP', 'PCP (Pneumocystis pneumonia)'),
        ('herpes', 'Herpes infection for more than one month'),
        (OTHER, ' OTHER, specify'),
        (NONE, ' None')],
    'member.transportmode': [
        ('Motor vehicle (car,truck,taxi, etc)',
         'Motor vehicle (car,truck,taxi, etc)'),
        ('Tractor', 'Tractor'),
        ('Bicycle', 'Bicycle'),
        ('Motorcycle/scooter', 'Motorcycle/scooter'),
        ('Donkey or cow cart', 'Donkey or cow cart'),
        ('Donkey/horses', 'Donkey/horses'),
        (OTHER, " OTHER, specify"),
        (NONE, ' None')],
    'member.electricalappliances': [
        ('radio', 'Radio'),
        ('tv', 'TV'),
        ('landline_telephone', 'Landline telephone'),
        ('cellphone', 'Cell phone'),
        ('computer', 'Computer'),
        ('access_to_internet', 'Access to internet'),
        ('refrigerator', 'Refrigerator'),
        (DWTA, " Don't want to answer"), ],
    'bcpp_subject.arv': [
        (OTHER, ' OTHER drug not listed: specify below ...'),
        ('Efavirenz', 'EFV (Stocrin, Sustiva)'),
        ('Dolutegravir', 'DTG (Tivicay)'),
        ('Tenofovir/emtricitabine', 'TDF/FTC (Truvada)'),
        ('Nevirapine', 'NVP (Viramune)'),
        ('Zidovudine/lamivudine', 'ZDV/3TC or AZT/3TC (Combivir)'),
        ('Lopinavir/ritonavir', 'LPV/r (Aluvia, Kaletra)'),
        ('Abacavir/lamivudine', 'ABC/3TC (Epzicom)'),
        ('Abacavir', 'ABC (Ziagen)'),
        ('Zidovudine', 'ZDV or AZT (Retrovir)'),
        ('Lamivudine', '3TC (Epivir)'),
        ('Atazanavir', 'ATV (Reyataz)'),
        ('Raltegravir', 'RAL (Isentress)'),
        ('Didanosine', 'ddI (Videx)'),
        ('Stavudine', 'D4T (Zerit)'),
        ('Tenofovir', 'TDF (Viread)'),
        ('Darunavir', 'DRV (Prezista)'),
        ('Saquinavir', 'SQV (Invirase)'),
        ('Ritonavir', 'RTV or r (Norvir)')],
    'bcpp_subject.hospitalizationreason': [
        ('Tuberculosis (TB, MTB)', 'Tuberculosis (TB, MTB)'),
        ('Pneumonia', 'Pneumonia'),
        ('Cryptococcal meningitis', 'Cryptococcal meningitis'),
        ('Immune Reconstitution Inflammatory Syndrome (IRIS)',
         'Immune Reconstitution Inflammatory Syndrome (IRIS)'),
        ('OTHER HIV-related illness', 'Other HIV-related illness'),
        ('Pregnancy-related care, including delivery',
         'Pregnancy-related care, including delivery'),
        ('Injury or accident', 'Injury or accident'),
        ('Medication toxicity', 'Medication toxicity'),
        ('Chronic disease related care', 'Chronic disease related care'),
        ('Stroke (or suspected stroke)', 'Stroke (or suspected stroke)'),
        (OTHER, ' OTHER (specify)'),
        (DONT_KNOW, " Don't know"),
    ],
    'bcpp_subject.chronicdisease': [
        ('High blood pressure', 'High blood pressure'),
        ('Diabetes', 'Diabetes'),
        ('Mental illness', 'Mental illness'),
    ]
}


for list_obj in list_data.keys():
    model = django_apps.get_app_config(
        list_obj.split('.')[0]).get_model(list_obj.split('.')[1])
    model.objects.all().delete()

for list_obj in list_data.keys():
    try:
        model = django_apps.get_app_config(
            list_obj.split('.')[0]).get_model(list_obj.split('.')[1])
        for tpl in list_data.get(list_obj):
            a, b = tpl
            try:
                obj = model.objects.get(short_name=a)
            except ObjectDoesNotExist:
                model.objects.create(short_name=a, name=b)
            else:
                obj.name = b
                obj.save()
    except Exception as e:
        print(e)
