from django.core.management.base import BaseCommand
from movie.models import News
import csv
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Load 5 news items from a Fake.csv-like dataset into the News model. Looks for Fake.csv in command folder or project root.'

    def handle(self, *args, **options):
        candidates = [
            os.path.join(os.path.dirname(__file__), 'Fake.csv'),
            os.path.join(os.getcwd(), 'Fake.csv'),
            os.path.join(os.getcwd(), 'fake.csv'),
        ]
        path = None
        for c in candidates:
            if os.path.exists(c):
                path = c
                break

        if not path:
            self.stdout.write(self.style.ERROR('Fake.csv not found. Place it in the project root or in movie/management/commands/'))
            return

        inserted = 0
        with open(path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                if inserted >= 5:
                    break
                # Common columns in the Fake news dataset: title, text, subject, date
                title = (row.get('title') or row.get('Title') or '').strip()
                text = (row.get('text') or row.get('content') or row.get('Text') or '').strip()
                url = (row.get('url') or '').strip()
                date_raw = (row.get('date') or row.get('Date') or '').strip()
                published = None
                if date_raw:
                    # Try the expected format: '%B %d, %Y' (e.g., January 1, 2019)
                    try:
                        published = datetime.strptime(date_raw, '%B %d, %Y')
                    except Exception:
                        # try common ISO format
                        try:
                            published = datetime.strptime(date_raw, '%Y-%m-%d')
                        except Exception:
                            published = None

                News.objects.create(
                    title=title or f'News {inserted+1}',
                    desc=text[:200],
                    image='',
                    url=url,
                    published=published
                )
                inserted += 1

        self.stdout.write(self.style.SUCCESS(f'Inserted {inserted} news items from {os.path.basename(path)}'))
