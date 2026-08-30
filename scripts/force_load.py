import os
import os
import csv
import sys

# Ensure project root is on sys.path so Python can import the Django project
sys.path.insert(0, os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviereviews.settings')
import django
django.setup()
from movie.models import Movie

CSV_PATH = os.path.join(os.getcwd(), 'movies_initial.csv')
if not os.path.exists(CSV_PATH):
    print('CSV not found at', CSV_PATH)
    sys.exit(1)

with open(CSV_PATH, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

if not rows:
    print('No rows found in CSV')
    sys.exit(1)

# delete existing
Movie.objects.all().delete()
print('Deleted existing Movie records')

count = 0
for r in rows:
    title = (r.get('title') or '').strip()
    if not title:
        continue
    movie = Movie(
        title=title,
        description=(r.get('description') or '').strip(),
        genre=(r.get('genre') or '').strip(),
        year=int(r['year']) if r.get('year') and r['year'].strip().isdigit() else None,
        url=(r.get('url') or '').strip()
    )
    movie.save()
    count += 1

print(f'Imported {count} movies')
print('Done. Now run: python manage.py runserver and open http://127.0.0.1:8000/')