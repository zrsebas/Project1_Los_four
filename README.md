# CineHub - Catálogo de Películas

## Descripción del Proyecto
**CineHub** es una aplicación web moderna para explorar y gestionar un catálogo de películas. La plataforma permite a los usuarios:

* **Navegar películas:** Visualizar un catálogo completo de películas con toda la información relevante
* **Información detallada:** Cada película muestra título, año, género, director y calificación
* **Noticias del cine:** Acceder a las últimas noticias y eventos del mundo cinematográfico
* **Análisis estadístico:** Visualizar gráficas interactivas de películas por año y género
* **Diseño responsivo:** Experiencia optimizada para dispositivos de cualquier tamaño

## Integrante
**Juan Sebastian Cortes Montoya**

## Características Principales

### 1. Catálogo de Películas
- Cards de Bootstrap con diseño atractivo
- Visualización de 15 películas iniciales desde CSV
- Información completa: título, año, género, director, calificación
- Efectos hover interactivos

### 2. Noticias del Cine
- Horizontal Cards de Bootstrap
- Última información sobre el mundo del cine
- Diseño responsivo y atractivo

### 3. Estadísticas
- Gráfica de barras: Películas por año
- Gráfica de dona: Películas por género
- Integración con Chart.js para visualización interactiva

### 4. Navbar Responsive
- Logo y navegación clara
- Menú desplegable en dispositivos móviles
- Enlaces a todas las secciones

## Tecnologías Utilizadas
* **Frontend:** HTML5, CSS3, JavaScript
* **Framework CSS:** Bootstrap 5.3
* **Gráficas:** Chart.js 4.4
* **Base de Datos:** CSV (movies_initial.csv)
* **Control de versiones:** Git y GitHub

## Estructura del Proyecto
```
CineHub/
├── index.html           # Página principal con catálogo de películas
├── news.html            # Página de noticias
├── charts.html          # Página de estadísticas
├── styles.css           # Estilos globales
├── script.js            # Lógica para cargar y mostrar películas
├── news-script.js       # Lógica para mostrar noticias
├── charts-script.js     # Lógica para crear gráficas
├── movies_initial.csv   # Dataset de películas
└── README.md            # Este archivo
```

## Cómo Usar
1. Clonar el repositorio
2. Abrir `index.html` en un navegador web
3. Explorar las diferentes secciones:
   - **Películas:** Catálogo completo con tarjetas interactivas
   - **Noticias:** Últimas noticias del cine
   - **Estadísticas:** Gráficas de análisis

## Datos de Películas
El dataset incluye 15 películas clásicas y contemporáneas con información detallada:
- The Shawshank Redemption (1994)
- The Godfather (1972)
- The Dark Knight (2008)
- Inception (2010)
- Y muchas más...

---
*Taller 2 - Programación Integrada 1 - EAFIT 2026*
