from datetime import datetime
from django.core.management.base import BaseCommand
from edc_reference.models import Reference


class Command(BaseCommand):

    help = 'Re-Saving reference data for sync'

    def handle(self, *args, **options):

        reference_data = Reference.objects.filter(
            report_datetime__gt=datetime(2017, 9, 9))
        total_reference_data = reference_data.count()
        count = 0
        for reference_dt in reference_data:
            reference_dt.save()
            count += 1
            self.stdout.write(self.style.SUCCESS(
                f'Succefully  re saved {count} out of {total_reference_data}.'))

        self.stdout.write(self.style.SUCCESS(
            f'Succefully Re-Saved {total_reference_data} reference data records.'))
