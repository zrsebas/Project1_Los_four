# Entrega 2 - Diseño de solución y preview de funcionalidad

## Proyecto: AhorraU

AhorraU es una aplicación web de finanzas personales para estudiantes universitarios. La preview implementa autenticación, registro de ingresos y egresos, cálculo de saldo, categorías, recomendaciones básicas y metas de ahorro.

## 1. Arquitectura y datos

### 1.1 Diagrama de despliegue

```mermaid
flowchart LR
  U["<<device>> Smartphone o PC\nNavegador web"] -->|HTTPS / JSON| W["<<node>> Servidor web\nPython 3.14 + Flask 3.1"]
  W -->|SQL local| DB["<<database>> SQLite 3\nfinanzas.db"]
  W -. opcional .-> AI["<<external node>> Google Gemini API\nHTTPS"]
```

| Nodo                      | Tecnología                                 | Responsabilidad                                                    |
| ------------------------- | ------------------------------------------ | ------------------------------------------------------------------ |
| Dispositivo cliente       | Navegador moderno, HTML5, CSS3, JavaScript | Interfaz responsive y captura de datos                             |
| Servidor web              | Python 3.14, Flask 3.1.1, Werkzeug         | Rutas, sesiones, validación y reglas de negocio                    |
| Persistencia              | SQLite 3                                   | Usuarios, transacciones y metas con claves foráneas                |
| Servicio externo opcional | Google Gemini API                          | Recomendaciones de lenguaje natural cuando exista `GEMINI_API_KEY` |
| Red                       | HTTPS/TLS en despliegue                    | Protección de datos en tránsito                                    |

### 1.2 Diagrama de componentes

```mermaid
flowchart LR
  UI["Componente UI\nTemplates + CSS"] --> AUTH["Componente Autenticación\nRegistro / Login / Sesión"]
  UI --> FIN["Componente Finanzas\nTransacciones / Saldo / Filtros"]
  UI --> GOALS["Componente Metas\nObjetivos / Progreso / Aportes"]
  FIN --> DB["Componente Persistencia\nSQLite + schema.sql"]
  GOALS --> DB
  AUTH --> DB
  FIN --> REC["Componente Recomendaciones\nReglas financieras"]
  REC -. opcional .-> GEM["Google Gemini API"]
```

| Componente      | Descripción                                                                         |
| --------------- | ----------------------------------------------------------------------------------- |
| UI              | Renderiza landing, autenticación y dashboard; adapta la vista a móvil y escritorio. |
| Autenticación   | Registra usuarios, hashea contraseñas y controla la sesión activa.                  |
| Finanzas        | Valida y persiste ingresos y egresos; calcula el saldo y los gastos por categoría.  |
| Metas           | Crea objetivos, registra aportes y calcula el porcentaje de progreso.               |
| Persistencia    | Aplica el esquema relacional y las restricciones de integridad.                     |
| Recomendaciones | Genera una sugerencia basada en el saldo, los egresos y la categoría dominante.     |

### 1.3 Modelo relacional

```mermaid
erDiagram
  USERS ||--o{ TRANSACTIONS : registra
  USERS ||--o{ SAVINGS_GOALS : define
  USERS {
    int id PK
    string email UK
    string password_hash
    datetime created_at
  }
  TRANSACTIONS {
    int id PK
    int user_id FK
    string type
    decimal amount
    string category
    string description
    date transaction_date
  }
  SAVINGS_GOALS {
    int id PK
    int user_id FK
    string name
    decimal target_amount
    decimal current_amount
    date deadline
  }
```

**Reglas:** todo movimiento y toda meta pertenece a un usuario; los montos son positivos; `type` solo acepta `income` o `expense`; eliminar un usuario elimina sus datos dependientes.

## 2. Mockups y preview

### Vista landing

* **Qué:** propuesta de valor, nombre AhorraU y llamados a crear una cuenta o iniciar sesión.
* **Dónde:** hero principal con tarjeta de saldo visual.
* **Cómo:** los botones llevan a los formularios de autenticación.

### Vista dashboard

* **Qué:** saldo, ingresos, gastos, actividad reciente, insight y metas.
* **Dónde:** métricas arriba; movimientos e insight al centro; formularios al final.
* **Cómo:** los formularios POST registran transacciones y crean metas sin salir del dashboard.

### Vista autenticación

* **Qué:** correo y contraseña.
* **Dónde:** panel central con un solo flujo.
* **Cómo:** validación de correo, contraseña mínima de 8 caracteres y mensajes de estado.

## 3. Repositorio

El repositorio debe contener este proyecto, `requirements.txt`, `README.md`, `schema.sql`, código, pruebas y la página Wiki. Cada integrante debe aportar al menos un commit descriptivo desde su usuario de GitHub.

## 4. Video (guion de 4:00 a 5:00)

1. **Pitch - 1:00:** integrantes, nombre AhorraU, problema de desorden financiero estudiantil, solución y estado actual: preview funcional con autenticación, movimientos, saldo, recomendaciones y metas.
2. **Explicación - 2:00:** mostrar FR01-FR06 (cuenta, login, ingreso, egreso, listado y saldo), FR14-FR15 (metas) y FR18 (recomendación); explicar que cada acción responde a una necesidad del estudiante.
3. **Evidencia - 2:00:** crear una cuenta, registrar un ingreso, registrar un egreso, mostrar el saldo y la categoría, crear una meta y revisar que la información persiste al recargar. Todos los integrantes aparecen en algún momento.

**Enlace:** pendiente de publicar en YouTube o Vimeo.

## 5. Gestión del proyecto

### Top 10 requisitos para Sprint 2

| Prioridad | Requisito                    | Estado                               | Responsable |
| --------: | ---------------------------- | ------------------------------------ | ----------- |
|         1 | FR01 Crear cuenta            | Implementado                         | Asignar     |
|         2 | FR02 Iniciar sesión          | Implementado                         | Asignar     |
|         3 | FR04 Registrar ingreso       | Implementado                         | Asignar     |
|         4 | FR05 Registrar egreso        | Implementado                         | Asignar     |
|         5 | FR06 Consultar transacciones | Implementado                         | Asignar     |
|         6 | FR09 Calcular saldo          | Implementado                         | Asignar     |
|         7 | FR14 Crear meta              | Implementado                         | Asignar     |
|         8 | FR15 Consultar progreso      | Implementado                         | Asignar     |
|         9 | FR18 Recomendaciones         | Implementado local; Gemini pendiente | Asignar     |
|        10 | UR05 Contraste WCAG AA       | Implementado visualmente; auditar    | Asignar     |

### Reuniones semanales

| Semana | Qué hicimos                                  | Qué haremos                        | Obstáculos                |
| ------ | -------------------------------------------- | ---------------------------------- | ------------------------- |
| 1      | Definimos usuarios, problema y requisitos    | Implementar modelo y autenticación | Confirmar responsables    |
| 2      | Construimos arquitectura y modelo relacional | Integrar dashboard y metas         | Disponibilidad del equipo |
| 3      | Validamos flujo principal y pruebas          | Grabar video y publicar Wiki       | Agendar grabación         |

### Retrospectiva Sprint 2

* **Continuar:** commits pequeños y descriptivos, validación temprana y decisiones documentadas.
* **Empezar:** revisar el tablero al inicio de cada reunión y asignar un responsable por requisito.
* **Detener:** acumular cambios sin integrar y dejar evidencias para el último día.

### Asignaciones de clase

Agregar aquí los enlaces o archivos de cada asignación solicitada por el curso, manteniendo una sección por actividad.
