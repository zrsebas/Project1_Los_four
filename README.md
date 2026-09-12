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
```

## Estructura

- `app.py`: rutas, autenticacion, reglas de saldo y persistencia.
- `schema.sql`: modelo relacional SQLite.
- `templates/`: vistas HTML de landing, autenticacion y dashboard.
- `static/app.css`: identidad visual responsive de la preview.
- `tests/`: pruebas de registro y transacciones.
- `WIKI_ENTREGA_2.md`: contenido listo para publicar en GitHub Wiki.

## Commits sugeridos para el equipo

Cada integrante debe realizar un commit descriptivo desde su cuenta. Ejemplos: `feat: agrega registro de transacciones`, `feat: implementa metas de ahorro`, `docs: documenta arquitectura y mockups`, `test: cubre flujo de registro`.

## Equipo y documentación

Este proyecto pertenece al equipo Los Four. La documentación técnica y de gestión está disponible en la [Wiki del repositorio](https://github.com/zrsebas/Project1_Los_four/wiki).

Integrantes: Juan Sebastián Cortés Montoya, Sebastián Zapata Rendón, Camilo Guzmán y David Ruiz.
