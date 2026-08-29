// Datos de noticias
const newsData = [
    {
        title: "Nuevo Récord en Taquilla",
        date: "28 de Agosto, 2026",
        description: "Las películas de ciencia ficción rompen nuevos récords de asistencia en cines de todo el mundo, demostrando el creciente interés del público por historias futuristas y aventuras épicas.",
        icon: "🎬"
    },
    {
        title: "Premios de Cine Anunciados",
        date: "25 de Agosto, 2026",
        description: "Los ganadores de los principales premios de cine internacional han sido anunciados, reconociendo las mejores películas, actores y directores del año en categorías como drama, comedia y acción.",
        icon: "🏆"
    },
    {
        title: "Nuevas Producciones en Desarrollo",
        date: "22 de Agosto, 2026",
        description: "Se anuncian varias películas emocionantes en desarrollo para los próximos años, incluyendo secuelas esperadas, remakes innovadores y adaptaciones de obras literarias clásicas.",
        icon: "🎥"
    },
    {
        title: "Tendencias en Cine Digital",
        date: "20 de Agosto, 2026",
        description: "La industria del cine adopta nuevas tecnologías digitales para mejorar la experiencia del espectador, incluyendo proyecciones en 4K, sonido envolvente y efectos visuales revolucionarios.",
        icon: "📽️"
    },
    {
        title: "Entrevista: Directores Destacados",
        date: "18 de Agosto, 2026",
        description: "Reconocidos directores de cine comparten sus perspectivas sobre la creatividad, el proceso de filmación y la evolución de la industria cinematográfica en la era digital.",
        icon: "🎭"
    }
];

// Función para mostrar noticias
function displayNews() {
    const container = document.getElementById('news-container');
    container.innerHTML = '';

    newsData.forEach(news => {
        const newsCard = document.createElement('div');
        newsCard.className = 'card news-card';
        newsCard.innerHTML = `
            <div class="row g-0">
                <div class="col-md-4">
                    <div class="news-image">
                        ${news.icon}
                    </div>
                </div>
                <div class="col-md-8">
                    <div class="card-body">
                        <h5 class="news-title">${news.title}</h5>
                        <p class="news-date">${news.date}</p>
                        <p class="news-description">${news.description}</p>
                        <a href="#" class="btn btn-sm btn-outline-primary">Leer más →</a>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(newsCard);
    });
}

// Cargar noticias cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', displayNews);
