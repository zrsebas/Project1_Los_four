from django.core.management.base import BaseCommand
import csv
import os
from movie.models import Movie


class Command(BaseCommand):
    help = 'Load movies from movies_initial.csv into the Movie model'

    def handle(self, *args, **options):
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        csv_path = os.path.join(base, '..', '..', 'movies_initial.csv')
        # resolve relative: project root is two levels up from app
        csv_path = os.path.normpath(os.path.join(base, '..', 'movies_initial.csv'))
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV not found at {csv_path}'))
            return

        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                title = (row.get('title') or '').strip()
                if not title:
                    continue
                defaults = {
                    'description': (row.get('description') or '').strip(),
                    'genre': (row.get('genre') or '').strip(),
                    'year': int(row['year']) if row.get('year') and row['year'].strip().isdigit() else None,
                    'url': (row.get('url') or '').strip()
                }
                obj, created = Movie.objects.update_or_create(title=title, defaults=defaults)
                if created:
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {count} movies'))
