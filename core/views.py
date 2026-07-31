from django.http import HttpResponse

def home(request):
    return HttpResponse("¡Hola! Este es mi primer taller funcionando en Django.")