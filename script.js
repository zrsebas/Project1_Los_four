// Datos de películas embebidos
const moviesData = [
    { title: "La Redención", year: 1994, genre: "Drama", rating: "9.3", director: "Frank Darabont" },
    { title: "El Padrino", year: 1972, genre: "Crimen|Drama", rating: "9.2", director: "Francis Ford Coppola" },
    { title: "El Caballero de la Noche", year: 2008, genre: "Acción|Crimen|Drama", rating: "9.0", director: "Christopher Nolan" },
    { title: "Tiempos Violentos", year: 1994, genre: "Crimen|Drama", rating: "8.9", director: "Quentin Tarantino" },
    { title: "Forrest Gump", year: 1994, genre: "Drama|Romance", rating: "8.8", director: "Robert Zemeckis" },
    { title: "Inicio", year: 2010, genre: "Acción|Ciencia Ficción|Suspenso", rating: "8.8", director: "Christopher Nolan" },
    { title: "El Club de la Pelea", year: 1999, genre: "Drama|Suspenso", rating: "8.8", director: "David Fincher" },
    { title: "Matrix", year: 1999, genre: "Acción|Ciencia Ficción", rating: "8.7", director: "The Wachowskis" },
    { title: "Buenos Muchachos", year: 1990, genre: "Crimen|Drama", rating: "8.7", director: "Martin Scorsese" },
    { title: "Interestelar", year: 2014, genre: "Aventura|Drama|Ciencia Ficción", rating: "8.6", director: "Christopher Nolan" },
    { title: "El Rey León", year: 1994, genre: "Animación|Aventura|Drama", rating: "8.5", director: "Roger Allers" },
    { title: "Parque Jurásico", year: 1993, genre: "Acción|Aventura|Ciencia Ficción", rating: "8.2", director: "Steven Spielberg" },
    { title: "Titánic", year: 1997, genre: "Drama|Romance", rating: "7.9", director: "James Cameron" },
    { title: "Avatar", year: 2009, genre: "Acción|Aventura|Fantasía|Ciencia Ficción", rating: "7.8", director: "James Cameron" },
    { title: "Los Vengadores", year: 2012, genre: "Acción|Aventura|Ciencia Ficción", rating: "8.0", director: "Joss Whedon" }
];

// Función para cargar películas
function loadMoviesFromCSV() {
    try {
        displayMovies(moviesData);
    } catch (error) {
        console.error('Error cargando películas:', error);
        document.getElementById('movies-container').innerHTML = 
            '<div class="alert alert-danger">Error cargando las películas</div>';
    }
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
