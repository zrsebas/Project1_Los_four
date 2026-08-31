# Taller 2 — CineApp

Proyecto listo para cumplir los 7 puntos de entrega del taller. Contiene:

- `index.html` — navbar + 3 vistas (Películas, Noticias, Gráficas)
- `movies_initial.csv` — dataset de 15 películas (title, year, genre, director, rating, synopsis, poster)
- `assets/app.js` — carga el CSV, dibuja las Cards de películas y las gráficas
- `assets/news.js` — datos de noticias para las Horizontal Cards
- `assets/styles.css` — estilos propios

## Cómo probarlo en tu computador

**Importante:** no abras `index.html` haciendo doble clic (protocolo `file://`), porque el `fetch()` del CSV falla por CORS. Debes servirlo con un servidor local:

```bash
# Dentro de la carpeta del proyecto
python3 -m http.server 8000
# luego abre http://localhost:8000 en el navegador
```

o con la extensión **Live Server** de VS Code (clic derecho sobre `index.html` → "Open with Live Server").

## Paso a paso para entregarlo en GitHub

1. Crea un repositorio nuevo en GitHub (o usa uno que ya tengas para la asignatura), por ejemplo `Taller2_TuNombre_PI1`.
2. Clónalo en tu computador:
   ```bash
   git clone https://github.com/TU_USUARIO/TU_REPO.git
   cd TU_REPO
   ```
3. Copia dentro todos los archivos de este proyecto (`index.html`, `movies_initial.csv`, la carpeta `assets/`, este `README.md`).
4. Crea la rama con tu nombre para el Taller 2:
   ```bash
   git checkout -b tu-nombre-taller2
   ```
5. Agrega y sube los cambios:
   ```bash
   git add .
   git commit -m "Taller 2: catálogo de películas, noticias y gráficas"
   git push -u origin tu-nombre-taller2
   ```
6. En GitHub, verifica que la rama `tu-nombre-taller2` (o como la hayas llamado) contenga todos los archivos.
7. Copia el enlace a esa rama (ej: `https://github.com/TU_USUARIO/TU_REPO/tree/tu-nombre-taller2`) y guárdalo para el formulario del punto 7.

## Cómo tomar cada captura pedida

| # | Requisito | Cómo hacerlo |
|---|-----------|--------------|
| 1 | Enlace a la rama | Copia la URL de la rama en GitHub después del `push`. |
| 2 | ≥10 películas en Cards, con navbar | Abre la vista "Películas" (la que carga por defecto), asegúrate de ver el navbar arriba y captura la pantalla completa. Ya hay 15 en el CSV. |
| 3 | Vista responsiva | Reduce el ancho de la ventana del navegador (o usa las DevTools en modo responsive) hasta que las cards se acomoden en 1 o 2 columnas, y captura con el navbar visible. |
| 4 | Noticias en Horizontal Cards | Haz clic en "Noticias" en el navbar y captura esa vista. |
| 5 | Gráfica por año | Haz clic en "Gráficas" y captura el gráfico de barras "Películas por año". |
| 6 | Gráfica por género | En la misma vista, captura el gráfico circular "Películas por género". |
| 7 | Formulario | Diligencia el formulario del taller con el enlace de tu rama (paso 7 del punto 1). |

## Notas

- Las imágenes de películas y noticias usan `picsum.photos` como *placeholder*; si tu profesor pide pósters reales, reemplaza las URLs en `movies_initial.csv` y en `assets/news.js` por imágenes propias o descargadas (guárdalas en `assets/img/` y referencia la ruta local).
- El buscador sobre las películas (`#movieSearch`) es un extra opcional, no es un requisito del taller, pero no estorba y puedes dejarlo o quitarlo.
- Si tu profesor exige usar exactamente los archivos del Taller 1 como base, copia estos archivos dentro de esa estructura y ajusta las rutas del navbar/menú a las que ya tenías.
