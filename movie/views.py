from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie
from django.db.models import Count
import json

# Create your views here.

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html')


def news(request):
    # Dynamic news from the News model (admin-editable), newest first
    from .models import News
    news_items = News.objects.order_by('-published')
    return render(request, 'news.html', {'news_items': news_items})


def movies_by_year(request):
    # Aggregate movie counts by year (X = year, Y = number of movies)
    qs = Movie.objects.order_by('year')

    # Build mapping year -> titles and counts
    year_map = {}
    for m in qs:
        key = str(m.year) if m.year is not None else 'Unknown'
        year_map.setdefault(key, []).append(m.title)

    # Prepare labels (sorted by year where possible) and values
    # Attempt to sort numeric years ascending, keep 'Unknown' at end
    numeric_years = sorted([int(y) for y in year_map.keys() if y != 'Unknown'])
    labels = [str(y) for y in numeric_years]
    if 'Unknown' in year_map:
        labels.append('Unknown')
    values = [len(year_map[y]) for y in labels]

    return render(request, 'movies_by_year.html', {
        'labels': json.dumps(labels),
        'values': json.dumps(values),
        'year_titles': json.dumps(year_map, ensure_ascii=False)
    })


def movies_by_genre(request):
    qs = Movie.objects.values('genre').annotate(count=Count('id')).order_by('-count')
    labels = [entry['genre'] if entry['genre'] else 'Unknown' for entry in qs]
    values = [entry['count'] for entry in qs]
    return render(request, 'movies_by_genre.html', {'labels': json.dumps(labels), 'values': json.dumps(values)})


def movies_by_movie(request):
    # Show each movie as an individual point (title -> year)
    qs = Movie.objects.order_by('title')
    labels = [m.title for m in qs]
    # Use 0 or null-safe conversion for year
    values = [m.year if m.year is not None else 0 for m in qs]
    return render(request, 'movies_by_movie.html', {'labels': json.dumps(labels), 'values': json.dumps(values)})