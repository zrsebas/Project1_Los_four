# AhorraU - Finanzas personales para estudiantes

AhorraU es una aplicacion web en Python para registrar ingresos y egresos, consultar el saldo, analizar categorias de gasto, crear metas de ahorro y recibir recomendaciones financieras.

## Requisitos

- Python 3.11 o superior
- pip

## Instalacion y ejecucion

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Abrir `http://127.0.0.1:5000`. La base `finanzas.db` y sus tablas se crean automaticamente al iniciar.

Para una clave de sesion propia, copiar `.env.example` como `.env` y definir `SECRET_KEY`.

## Pruebas

```powershell
pytest -q
- Git

## Clonar el repositorio

Desde PowerShell o una terminal, ejecuta:

```powershell
git clone https://github.com/zrsebas/Project1_Los_four.git
cd Project1_Los_four
```

Si ya tienes el proyecto clonado, actualiza tu copia local con:

```powershell
```
```

## Instalacion y ejecucion en Windows

Python no necesita una compilacion tradicional. El programa se ejecuta con el interprete de Python.

1. Crea un entorno virtual:

- `app.py`: rutas, autenticacion, reglas de saldo y persistencia.
- `schema.sql`: modelo relacional SQLite.
- `templates/`: vistas HTML de landing, autenticacion y dashboard.
```

2. Instala las dependencias:

```powershell
- `static/app.css`: identidad visual responsive de la preview.
```

3. Configura las variables opcionales:

```powershell
Copy-Item .env.example .env
```

Puedes editar `.env` y cambiar `SECRET_KEY` por una clave propia.

4. Inicia la aplicación:

```powershell
- `tests/`: pruebas de registro y transacciones.
- `WIKI_ENTREGA_2.md`: contenido listo para publicar en GitHub Wiki.

Abre `http://127.0.0.1:5000` en el navegador. La base `finanzas.db` y sus tablas se crean automaticamente al iniciar.

Para detener el servidor, presiona `Ctrl+C` en la terminal.

## Instalacion en macOS o Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Luego abre `http://127.0.0.1:5000`.

## Ejecutar pruebas

Este proyecto pertenece al equipo Los Four. La documentación técnica y de gestión está disponible en la [Wiki del repositorio](https://github.com/zrsebas/Project1_Los_four/wiki).
python -m pytest -q
Integrantes: Juan Sebastián Cortés Montoya, Sebastián Zapata Rendón, Camilo Guzmán y David Ruiz.

El comando debe mostrar todas las pruebas aprobadas.

## Actualizar el repositorio

Despues de realizar cambios, ejecuta:

```powershell
git add .
git commit -m "descripcion breve del cambio"
git push origin main
```

Los integrantes del equipo pueden obtener esos cambios con `git pull origin main`.
