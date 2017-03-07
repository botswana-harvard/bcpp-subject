from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        from bcpp_subject.list_data import list_data
        from bcpp_subject.groups import groups
        print("Loaded {} crf lists".format(len(list_data)))
