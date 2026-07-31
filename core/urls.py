from django.urls import path
from .views import home, about, lista_peliculas, buscar_pelicula

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('peliculas/', lista_peliculas, name='lista_peliculas'),
    path('buscar/', buscar_pelicula, name='buscar_pelicula'),
]