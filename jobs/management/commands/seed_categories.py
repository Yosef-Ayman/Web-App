from django.core.management.base import BaseCommand

from jobs.models import JobCategory

DEFAULT_CATEGORIES = [
    'Information Technology',
    'Sales',
    'Marketing',
    'Design',
    'Finance',
    'Engineering',
    'Human Resources',
]


class Command(BaseCommand):
    help = 'Seed default job categories'

    def handle(self, *args, **options):
        created = 0
        for name in DEFAULT_CATEGORIES:
            _, was_created = JobCategory.objects.get_or_create(name=name)
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {created} new categories.'))
