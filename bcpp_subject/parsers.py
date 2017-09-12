from edc_sync.parsers import datetime_to_date_parser


def schedule_appt_date_parser(self, json_text=None):
    """A JSON text parser to fix a subjectreferral.schedule_appt_date
    incorrectly set to a datetime in older transactions.
    """
    model = 'bcpp_subject.subjectreferral'
    field = 'schedule_appt_date'
    return datetime_to_date_parser(json_text, model=model, field=field)
