from edc_base.utils import age


def is_minor(dob, reference_datetime):
    return 16 <= age(dob, reference_datetime).years < 18
