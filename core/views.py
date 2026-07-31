from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Bienvenido al Taller de Juan sebastian Cortes montoya</h1><p>Este es mi proyecto base funcionando en Django.</p>")

def about(request):
    return HttpResponse("<h1>Acerca de nosotros</h1><p>Esta es la página de información del proyecto de taller.</p>")

from .models import Pelicula

def lista_peliculas(request):
    peliculas = Pelicula.objects.all()
    html = "<h1>Lista de Películas</h1><ul>"
    for p in peliculas:
        html += f"<li>{p.titulo} - Dirigida por: {p.director}</li>"
    html += "</ul>"
    return HttpResponse(html)

def buscar_pelicula(request):
    query = request.GET.get('q', '')
    peliculas = Pelicula.objects.filter(titulo__icontains=query) if query else []
    
    html = """
    <h1>Buscar Película</h1>
    <form method="GET">
        <input type="text" name="q" placeholder="Nombre de película..." value=""" + f'"{query}"' + """>
        <button type="submit">Buscar</button>
    </form>
    <ul>
    """
    for p in peliculas:
        html += f"<li>{p.titulo} - Dirigida por: {p.director}</li>"
    html += "</ul>"
    return HttpResponse(html)