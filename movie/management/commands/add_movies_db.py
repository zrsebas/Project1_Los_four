from django.core.management.base import BaseCommand
from movie.models import Movie
import csv
import os


class Command(BaseCommand):
    help = 'Load movies from a CSV into the Movie model. Looks for movies_initial.csv in the command folder or project root.'

    def handle(self, *args, **options):
        candidates = [
            os.path.join(os.path.dirname(__file__), 'movies_initial.csv'),
            os.path.join(os.getcwd(), 'movies_initial.csv'),
        ]
        path = None
        for c in candidates:
            if os.path.exists(c):
                path = c
                break

        if not path:
            self.stdout.write(self.style.ERROR('movies_initial.csv not found. Place it in the project root or in movie/management/commands/'))
            return

        imported = 0
        with open(path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                title = (row.get('title') or row.get('Title') or row.get('name') or '').strip()
                if not title:
                    continue
                description = (row.get('description') or row.get('desc') or row.get('overview') or '').strip()
                image = (row.get('image') or row.get('poster') or '').strip()
                url = (row.get('url') or row.get('link') or '').strip()
                genre = (row.get('genre') or row.get('genres') or '').strip()
                year_raw = (row.get('year') or row.get('Year') or '').strip()
                try:
                    year = int(year_raw) if year_raw else None
                except Exception:
                    year = None

                Movie.objects.update_or_create(
                    title=title,
                    defaults={
                        'description': description,
                        'image': image,
                        'url': url,
                        'genre': genre,
                        'year': year,
                    }
                )
                imported += 1

        self.stdout.write(self.style.SUCCESS(f'Imported/updated {imported} movies from {os.path.basename(path)}'))
