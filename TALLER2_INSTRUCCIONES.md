Taller 2 — Instrucciones para ejecución y capturas

Resumen
- Este repo contiene las plantillas y vistas necesarias para generar las capturas solicitadas: listado en Cards, News en Horizontal Cards, y gráficas por año y por género.

Pasos para preparar el entorno y poblar la BD
1. Crear migraciones y aplicar:

```bash
python manage.py makemigrations
python manage.py migrate
```

2. Cargar el dataset de ejemplo (incluido `movies_initial.csv` con 10 películas):

```bash
python manage.py load_movies
```

3. Ejecutar el servidor de desarrollo:

```bash
python manage.py runserver
```

Rutas importantes
- Home (Cards): http://127.0.0.1:8000/
- News (Horizontal Cards): http://127.0.0.1:8000/news/
- Gráfica por año: http://127.0.0.1:8000/charts/year/
- Gráfica por género: http://127.0.0.1:8000/charts/genre/

Requisitos de las capturas (entregables)
1. Captura con al menos 10 películas cargadas desde `movies_initial.csv`:
   - Abre `http://127.0.0.1:8000/`.
   - Asegúrate de haber ejecutado `python manage.py load_movies`.
   - La página muestra las películas en Bootstrap Cards; cada Card debe mostrar `title`, `description`, `genre` y `year`.
   - La captura debe incluir el navbar con la imagen estática (logo en `movie/static/movie/logo.svg`).

2. Captura en tamaño pequeño (responsive):
   - Con la misma página `http://127.0.0.1:8000/`, reduce la ventana del navegador o usa las herramientas de desarrollador → Responsive Design Mode.
   - Recomendación de tamaños: ancho 360px (móvil) o 768px (tablet). La captura debe mostrar el navbar y que las Cards se adapten.

3. Captura de `News` con Horizontal Cards:
   - Abre `http://127.0.0.1:8000/news/`.
   - Asegúrate de que las noticias aparezcan en Cards horizontales (plantilla `movie/templates/news.html`).

4. Captura de la gráfica por año:
   - Abre `http://127.0.0.1:8000/charts/year/`.
   - La gráfica está implementada con Chart.js y toma los datos desde la BD.

5. Captura de la gráfica por género:
   - Abre `http://127.0.0.1:8000/charts/genre/`.

Consejos para capturas de calidad
- Usa el modo sin marca de la ventana del navegador si es posible (maximiza la vista y evita overlays).
- Resoluciones recomendadas:
  - Desktop: 1366×768 o 1920×1080
  - Mobile: 360×800 o 375×812 (iPhone)
- Asegúrate de que el navbar con el logo esté visible en cada captura.
- Para la captura en tamaño pequeño, abre DevTools (F12) → Toggle device toolbar (Ctrl+Shift+M) y selecciona un tamaño móvil.

Control de versiones (subir a la rama de entrega)
1. Crear y cambiar a la rama de entrega (por ejemplo `taller2`):

```bash
git checkout -b taller2
```

2. Añadir y commitear los cambios:

```bash
git add .
git commit -m "Taller 2: cards, news, charts, loader CSV e instrucciones"
```

3. Subir la rama al remoto:

```bash
git push -u origin taller2
```

Archivos clave que modifiqué/añadí
- `movie/models.py` — agregué campos `genre` y `year` y permití `image` vacío.
- `movie/views.py` — nuevas vistas `news`, `movies_by_year`, `movies_by_genre`.
- `moviereviews/urls.py` — rutas añadidas para news y charts.
- `movie/templates/base.html` — navbar con logo estático.
- `movie/templates/home.html` — muestra las películas en Cards (muestra `genre` y `year`).
- `movie/templates/news.html` — noticias en Horizontal Cards.
- `movie/templates/movies_by_year.html` — Chart.js (bar).
- `movie/templates/movies_by_genre.html` — Chart.js (pie).
- `movie/management/commands/load_movies.py` — comando para cargar `movies_initial.csv`.
- `movies_initial.csv` — dataset con 10 películas de ejemplo.
- `movie/static/movie/logo.svg` — logo del navbar.

Si quieres, puedo:
- Preparar un README listo para subir a la rama y un archivo ZIP con las capturas ya generadas (necesito que me proporciones las imágenes si quieres que las incluya),
- O guiarte paso a paso mientras ejecutas los comandos para generar las capturas y verificar los requisitos.

