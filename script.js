// Función para cargar el CSV
async function loadMoviesFromCSV() {
    try {
        const response = await fetch('movies_initial.csv');
        const csvText = await response.text();
        const movies = parseCSV(csvText);
        displayMovies(movies);
    } catch (error) {
        console.error('Error cargando películas:', error);
        document.getElementById('movies-container').innerHTML = 
            '<div class="alert alert-danger">Error cargando las películas</div>';
    }
}

// Función para parsear el CSV
function parseCSV(csvText) {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',');
    const movies = [];

    for (let i = 1; i < lines.length; i++) {
        const obj = {};
        const currentLine = lines[i].split(',');

        for (let j = 0; j < headers.length; j++) {
            obj[headers[j]] = currentLine[j];
        }
        movies.push(obj);
    }

    return movies;
}

// Función para mostrar las películas
function displayMovies(movies) {
    const container = document.getElementById('movies-container');
    container.innerHTML = '';

    movies.forEach((movie, index) => {
        const genreList = movie.genre.split('|').map(g => g.trim()).join(', ');
        const filmEmoji = ['🎬', '🎭', '🎪', '🎨', '📽️', '🎥', '🎞️', '🎟️', '🏆', '✨'][index % 10];

        const movieCard = document.createElement('div');
        movieCard.className = 'col-lg-3 col-md-4 col-sm-6 col-12';
        movieCard.innerHTML = `
            <div class="card movie-card">
                <div class="movie-poster">
                    ${filmEmoji}
                </div>
                <div class="card-body">
                    <h5 class="card-title movie-title">${movie.title}</h5>
                    <div class="movie-attribute">
                        <label>Año:</label> ${movie.year}
                    </div>
                    <div class="movie-attribute">
                        <label>Género:</label> ${genreList}
                    </div>
                    <div class="movie-attribute">
                        <label>Director:</label> ${movie.director}
                    </div>
                    <div class="movie-attribute mt-2">
                        <label>Calificación:</label> <span class="movie-rating">⭐ ${movie.rating}</span>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(movieCard);
    });
}

// Cargar películas cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', loadMoviesFromCSV);
