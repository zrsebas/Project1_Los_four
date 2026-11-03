# AhorraU

AhorraU es una aplicación web desarrollada en Python con Flask para ayudar a estudiantes universitarios a controlar ingresos, egresos, metas de ahorro y recomendaciones financieras de forma simple y clara.

## Funcionalidades principales

- Registro e inicio de sesión de usuarios.
- Gestión de sueldo mensual.
- Registro de ingresos y egresos.
- Categorización de dinero reservado y gastos.
- Cálculo de saldo disponible.
- Creación y seguimiento de metas de ahorro.
- Recomendaciones financieras basadas en el comportamiento del usuario.
- Persistencia de datos con SQLite.

## Stack tecnológico

- Python 3.11+
- Flask 3.1.1
- SQLite 3
- Pytest 8.4.1
- python-dotenv 1.1.0

## Requisitos previos

- Python 3.11 o superior
- pip
- Git

## Instalación

### Windows

```powershell
cd "ruta\al\proyecto"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

### macOS / Linux

```bash
cd /ruta/al/proyecto
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

La aplicación queda disponible en:

```text
http://127.0.0.1:5000
```

## Despliegue de demostración en AWS EC2

Estos pasos son para la aplicación Flask de este repositorio (no para Django). En el grupo de seguridad de la instancia, agrega una regla TCP entrante para el puerto `8000`. Para una demostración académica puedes permitir el acceso desde cualquier dirección; no uses esta configuración para información sensible o producción.

Conéctate a la instancia Amazon Linux 2023 mediante EC2 Instance Connect y ejecuta:

```bash
sudo dnf install -y python3.11 python3.11-pip git
git clone <URL_DEL_REPOSITORIO>
cd <CARPETA_DEL_REPOSITORIO>
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="$(python3.11 -c 'import secrets; print(secrets.token_hex(32))')"
gunicorn --bind 0.0.0.0:8000 --workers 2 app:app
```

Reemplaza la URL y el nombre de carpeta por los de tu repositorio. Mientras Gunicorn siga ejecutándose, abre `http://<IP_PUBLICA_EC2>:8000` en el navegador. Detén el servidor con `Ctrl+C` y luego detén la instancia desde EC2 para cerrar la demostración.

La base de datos SQLite se crea en la instancia al iniciar la app y no se sube a GitHub. Este procedimiento es para una demostración temporal; para un servicio permanente se debe configurar un servidor WSGI como servicio y HTTPS.

## Variables de entorno

El proyecto incluye el archivo `.env.example` con estas variables:

```env
SECRET_KEY=change-this-in-production
GEMINI_API_KEY=
```

`SECRET_KEY` es opcional para el funcionamiento local, pero se recomienda definir una clave propia en producción.

La recomendación de Gemini se activa al definir `GEMINI_API_KEY`. Crea la clave en Google AI Studio y guárdala en el archivo `.env` local o como variable de entorno en EC2 antes de iniciar Gunicorn:

```bash
export GEMINI_API_KEY="TU_CLAVE_DE_GOOGLE_AI_STUDIO"
```

No subas la clave a GitHub ni la compartas en capturas. La aplicación envía a Gemini solo el saldo, los egresos acumulados y los montos agrupados por categoría; no envía correo, contraseña ni descripciones de transacciones. Si la clave no está configurada o Gemini no responde, se muestra la recomendación local de respaldo.

## Ejecutar pruebas

```powershell
.\.venv\Scripts\python -m pytest -q
```

O, en Linux/macOS:

```bash
python -m pytest -q
```

## Estructura del proyecto

```text
app.py
schema.sql
requirements.txt
README.md
.env.example
static/
templates/
tests/
WIKI_ENTREGA_2.md
WIKI_ENTREGA_3.md
```

## Equipo

- Juan Sebastián Cortés Montoya
- Sebastián Zapata Rendón
- Camilo Guzmán
- David Ruiz

## Diferencia con la entrega anterior

La entrega 2 dejó la base conceptual y la preview funcional; la entrega 3 consolida el MVP con validación, documentación, identidad visual y seguimiento de gestión del proyecto.
