// Datos de películas
const moviesData = [
    { title: "The Shawshank Redemption", year: 1994, genre: "Drama" },
    { title: "The Godfather", year: 1972, genre: "Crime" },
    { title: "The Dark Knight", year: 2008, genre: "Action" },
    { title: "Pulp Fiction", year: 1994, genre: "Crime" },
    { title: "Forrest Gump", year: 1994, genre: "Drama" },
    { title: "Inception", year: 2010, genre: "Sci-Fi" },
    { title: "Fight Club", year: 1999, genre: "Drama" },
    { title: "The Matrix", year: 1999, genre: "Sci-Fi" },
    { title: "Goodfellas", year: 1990, genre: "Crime" },
    { title: "Interstellar", year: 2014, genre: "Sci-Fi" },
    { title: "The Lion King", year: 1994, genre: "Animation" },
    { title: "Jurassic Park", year: 1993, genre: "Sci-Fi" },
    { title: "Titanic", year: 1997, genre: "Drama" },
    { title: "Avatar", year: 2009, genre: "Sci-Fi" },
    { title: "The Avengers", year: 2012, genre: "Action" }
];

// Función para contar películas por año
function countMoviesByYear() {
    const yearCount = {};
    moviesData.forEach(movie => {
        yearCount[movie.year] = (yearCount[movie.year] || 0) + 1;
    });
    return yearCount;
}

// Función para contar películas por género
function countMoviesByGenre() {
    const genreCount = {};
    moviesData.forEach(movie => {
        const genres = movie.genre.split('|').map(g => g.trim());
        genres.forEach(genre => {
            genreCount[genre] = (genreCount[genre] || 0) + 1;
        });
    });
    return genreCount;
}

// Crear gráfica de películas por año
function createYearChart() {
    const yearData = countMoviesByYear();
    const sortedYears = Object.keys(yearData).sort((a, b) => a - b);
    const counts = sortedYears.map(year => yearData[year]);

    const ctx = document.getElementById('chartByYear').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedYears,
            datasets: [{
                label: 'Cantidad de Películas',
                data: counts,
                backgroundColor: 'rgba(229, 9, 20, 0.8)',
                borderColor: 'rgba(229, 9, 20, 1)',
                borderWidth: 2,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: Math.max(...counts) + 1
                }
            }
        }
    });
}

// Crear gráfica de películas por género
function createGenreChart() {
    const genreData = countMoviesByGenre();
    const genres = Object.keys(genreData).sort();
    const counts = genres.map(genre => genreData[genre]);

    const ctx = document.getElementById('chartByGenre').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: genres,
            datasets: [{
                data: counts,
                backgroundColor: [
                    'rgba(229, 9, 20, 0.8)',
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(118, 75, 162, 0.8)',
                    'rgba(255, 159, 64, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 205, 86, 0.8)',
                    'rgba(201, 203, 207, 0.8)'
                ],
                borderColor: 'rgba(255, 255, 255, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

// Inicializar gráficas cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    createYearChart();
    createGenreChart();
});
