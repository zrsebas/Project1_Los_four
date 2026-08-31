// ============================================================
// Taller 2 - Lógica principal de la aplicación
// ============================================================

let allMovies = [];

// Colores por género para los pósters generados localmente
const genreColors = {
  "Sci-Fi": "#3b5bdb",
  "Drama": "#862e2e",
  "Horror": "#1a1a1a",
  "Comedy": "#e8a63a"
};

// Imagen de respaldo genérica para las noticias, generada localmente
function newsFallback() {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200">
      <rect width="300" height="200" fill="#343a40"/>
      <text x="150" y="105" font-family="Arial" font-size="18" fill="white" text-anchor="middle">CineApp</text>
    </svg>`;
  return "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svg)));
}

// Genera un póster localmente (SVG en base64) para no depender de internet
function makeLocalPoster(title, genre) {
  const color = genreColors[genre] || "#495057";
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="400" height="600">
      <rect width="400" height="600" fill="${color}"/>
      <text x="200" y="280" font-family="Arial, sans-serif" font-size="26"
            fill="white" text-anchor="middle" font-weight="bold">${genre}</text>
      <foreignObject x="30" y="320" width="340" height="200">
        <div xmlns="http://www.w3.org/1999/xhtml"
             style="color:white;font-family:Arial,sans-serif;font-size:22px;
                    text-align:center;font-weight:bold;">${title}</div>
      </foreignObject>
    </svg>`;
  return "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svg)));
}

// ---------- 1. Parseo simple del CSV ----------
function parseCSV(text) {
  const lines = text.trim().split("\n");
  const headers = lines[0].split(",").map(h => h.trim());

  return lines.slice(1).map(line => {
    const values = line.split(",");
    const movie = {};
    headers.forEach((h, i) => {
      movie[h] = (values[i] || "").trim();
    });
    return movie;
  });
}

// ---------- 2. Renderizar tarjetas de películas (Bootstrap Cards) ----------
function renderMovies(movies) {
  const container = document.getElementById("moviesContainer");
  const countEl = document.getElementById("movieCount");
  container.innerHTML = "";

  movies.forEach((movie, index) => {
    const col = document.createElement("div");
    col.className = "col";
    col.innerHTML = `
      <div class="card h-100 shadow-sm movie-card">
        <img src="${movie.poster}" class="card-img-top" alt="Póster de ${movie.title}"
             onerror="this.onerror=null;this.src='${makeLocalPoster(movie.title, movie.genre)}';">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title">${movie.title}</h5>
          <div class="mb-2">
            <span class="badge text-bg-primary">${movie.genre}</span>
            <span class="badge text-bg-secondary">${movie.year}</span>
            <span class="badge text-bg-warning text-dark">&#9733; ${movie.rating}</span>
          </div>
          <p class="card-text small text-secondary mb-1"><strong>Director:</strong> ${movie.director}</p>
          <p class="card-text small flex-grow-1">${movie.synopsis}</p>
        </div>
      </div>
    `;
    container.appendChild(col);
  });

  countEl.textContent = `${movies.length} película(s) encontradas`;
}

// ---------- 3. Renderizar tarjetas horizontales de noticias ----------
function renderNews(news) {
  const container = document.getElementById("newsContainer");
  container.innerHTML = "";

  news.forEach(item => {
    const card = document.createElement("div");
    card.className = "card news-card shadow-sm";
    card.innerHTML = `
      <div class="row g-0">
        <div class="col-md-3">
          <img src="${item.image}" class="img-fluid rounded-start w-100" alt="${item.title}"
               onerror="this.onerror=null;this.src=newsFallback();">
        </div>
        <div class="col-md-9">
          <div class="card-body">
            <h5 class="card-title">${item.title}</h5>
            <p class="card-text"><small class="text-body-secondary">${item.date}</small></p>
            <p class="card-text">${item.summary}</p>
          </div>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

// ---------- 4. Gráficas con Chart.js ----------
function renderCharts(movies) {
  // Conteo por año
  const byYear = {};
  movies.forEach(m => { byYear[m.year] = (byYear[m.year] || 0) + 1; });
  const years = Object.keys(byYear).sort();

  new Chart(document.getElementById("chartByYear"), {
    type: "bar",
    data: {
      labels: years,
      datasets: [{
        label: "Cantidad de películas",
        data: years.map(y => byYear[y]),
        backgroundColor: "#0d6efd"
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
    }
  });

  // Conteo por género
  const byGenre = {};
  movies.forEach(m => { byGenre[m.genre] = (byGenre[m.genre] || 0) + 1; });
  const genres = Object.keys(byGenre);

  new Chart(document.getElementById("chartByGenre"), {
    type: "pie",
    data: {
      labels: genres,
      datasets: [{
        label: "Cantidad de películas",
        data: genres.map(g => byGenre[g]),
        backgroundColor: ["#0d6efd", "#dc3545", "#ffc107", "#198754", "#6610f2", "#fd7e14"]
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: "bottom" } }
    }
  });
}

// ---------- 5. Buscador de películas ----------
document.getElementById("movieSearch").addEventListener("input", (e) => {
  const term = e.target.value.toLowerCase();
  const filtered = allMovies.filter(m =>
    m.title.toLowerCase().includes(term) || m.genre.toLowerCase().includes(term)
  );
  renderMovies(filtered);
});

// ---------- 6. Navegación entre vistas ----------
document.querySelectorAll("[data-view]").forEach(link => {
  link.addEventListener("click", (e) => {
    e.preventDefault();
    document.querySelectorAll("[data-view]").forEach(l => l.classList.remove("active"));
    link.classList.add("active");

    ["movies-view", "news-view", "charts-view"].forEach(id => {
      document.getElementById(id).classList.add("d-none");
    });
    document.getElementById(link.dataset.view).classList.remove("d-none");
  });
});

// ---------- 7. Carga inicial ----------
fetch("movies_initial.csv")
  .then(res => res.text())
  .then(text => {
    allMovies = parseCSV(text);
    renderMovies(allMovies);
    renderCharts(allMovies);
  })
  .catch(err => {
    document.getElementById("moviesContainer").innerHTML =
      `<div class="alert alert-danger">No se pudo cargar movies_initial.csv: ${err}</div>`;
  });

renderNews(newsData);
