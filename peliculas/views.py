from django.shortcuts import render

peliculas = [
    {
        "titulo": "El Conjuro",
        "categoria": "Terror",
        "descripcion": "Dos investigadores paranormales ayudan a una familia que vive aterrorizada por una presencia maligna dentro de su hogar.",
        "imagen": "https://picsum.photos/280/390?random=11"
    },
    {
        "titulo": "It",
        "categoria": "Terror",
        "descripcion": "Un antiguo mal toma la forma de un payaso para sembrar el miedo en un pequeño pueblo.",
        "imagen": "https://picsum.photos/280/390?random=12"
    },
    {
        "titulo": "¿Qué pasó ayer?",
        "categoria": "Comedia",
        "descripcion": "Tres amigos viven una aventura caótica tratando de reconstruir la noche más loca de sus vidas.",
        "imagen": "https://picsum.photos/280/390?random=13"
    },
    {
        "titulo": "Mi Villano Favorito",
        "categoria": "Comedia",
        "descripcion": "Gru descubre que la familia puede cambiar incluso al villano más temido.",
        "imagen": "https://picsum.photos/280/390?random=14"
    },
    {
        "titulo": "Frozen",
        "categoria": "Disney",
        "descripcion": "Anna emprende una aventura para encontrar a Elsa y salvar su reino.",
        "imagen": "https://picsum.photos/280/390?random=15"
    },
    {
        "titulo": "El Rey León",
        "categoria": "Disney",
        "descripcion": "Simba deberá enfrentar su destino para convertirse en el verdadero rey.",
        "imagen": "https://picsum.photos/280/390?random=16"
    },
    {
        "titulo": "John Wick",
        "categoria": "Acción",
        "descripcion": "Un legendario asesino vuelve al mundo criminal en busca de justicia y venganza.",
        "imagen": "https://picsum.photos/280/390?random=17"
    },
    {
        "titulo": "Avengers: Endgame",
        "categoria": "Acción",
        "descripcion": "Los héroes restantes unen fuerzas para la batalla definitiva por el universo.",
        "imagen": "https://picsum.photos/280/390?random=18"
    }
]

def inicio(request):
    buscar = request.GET.get("buscar", "")

    if buscar:
        resultado = [
            p for p in peliculas
            if buscar.lower() in p["titulo"].lower()
        ]
    else:
        resultado = peliculas

    return render(request, "index.html", {
        "peliculas": resultado,
        "buscar": buscar
    })


def about(request):
    return render(request, "about.html")