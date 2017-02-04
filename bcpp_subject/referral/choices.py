REFERRAL_CODES = (
    ('pending', '<data collection in progress>'),
    ('TST-CD4', 'POS any, need CD4 testing'),
    ('TST-HIV', 'HIV test'),
    ('MASA-CC', 'Known POS, MASA continued care'),
    ('MASA-DF', 'Known POS, MASA defaulter (was on ART)'),
    ('SMC-NEG', 'SMC (uncircumcised, hiv neg)'),
    ('SMC?NEG', 'SMC (Unknown circumcision status, hiv neg'),
    ('SMC-UNK', 'SMC (uncircumcised, hiv result not known)'),
    ('SMC?UNK', 'SMC (Unknown circumcision status, hiv result not known)'),
    ('NEG!-PR', 'NEG today, Pregnant'),
    ('POS!-PR', 'POS today, Pregnant'),
    ('UNK?-PR', 'HIV UNKNOWN, Pregnant'),
    ('POS#-AN', 'Known POS, Pregnant, on ART (ANC)'),
    ('POS#-PR', 'Known POS, Pregnant, not on ART'),
    ('POS!-HI', 'POS today, not on ART, high CD4)'),
    ('POS!-LO', 'POS today, not on ART, low CD4)'),
    ('POS#-HI', 'Known POS, not on ART, high CD4)'),
    ('POS#-LO', 'Known POS, not on ART, low CD4)'),
)

REFERRAL_CLINIC_TYPES = (
    ('ANC', 'ANC'),
    ('IDCC', 'IDCC'),
    ('SMC', 'SMC'),
    ('VCT', 'VCT'),
)
