# API de Notas - Backend

Backend desarrollado con Python y Flask para una aplicación de notas con conexión a PostgreSQL.

## Estructura del Proyecto

```
notas-backend/
├── app.py                  # Aplicación principal
├── config/
│   ├── __init__.py
│   └── database.py         # Configuración de PostgreSQL
├── models/
│   ├── __init__.py
│   └── note.py             # Modelo de Nota
├── controllers/
│   ├── __init__.py
│   └── note_controller.py  # Controlador de endpoints
├── requirements.txt        # Dependencias
├── .env.example           # Ejemplo de variables de entorno
├── .gitignore
└── README.md
```

## Requisitos Previos

- Python 3.8 o superior
- PostgreSQL instalado y corriendo
- pip (gestor de paquetes de Python)

## Configuración

### 1. Crear base de datos en PostgreSQL

```sql
CREATE DATABASE notas_db;
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus credenciales:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus datos:

```
DB_HOST=localhost
DB_NAME=notas_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_PORT=5432
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

El servidor se ejecutará en `http://localhost:5000`

## Endpoints de la API

### 1. GET - Obtener todas las notas de un usuario

**Endpoint:** `GET /api/notes/<user_id>`

**Respuesta exitosa:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Mi primera nota",
      "content": "Contenido de la nota",
      "user_id": "usuario123",
      "created_at": "2025-12-11T10:30:00",
      "updated_at": "2025-12-11T10:30:00"
    }
  ],
  "count": 1
}
```

### 2. POST - Crear una nueva nota

**Endpoint:** `POST /api/notes/`

**Body (JSON):**
```json
{
  "title": "Título de la nota",
  "content": "Contenido de la nota",
  "user_id": "usuario123"
}
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Título de la nota",
    "content": "Contenido de la nota",
    "user_id": "usuario123",
    "created_at": "2025-12-11T10:30:00",
    "updated_at": "2025-12-11T10:30:00"
  },
  "message": "Nota creada exitosamente"
}
```

## Tecnologías Utilizadas

- **Flask**: Framework web minimalista
- **PostgreSQL**: Base de datos relacional
- **psycopg2**: Adaptador de PostgreSQL para Python
- **flask-cors**: Manejo de CORS
- **python-dotenv**: Gestión de variables de entorno

## Características

- ✅ Arquitectura MVC (Modelo-Vista-Controlador)
- ✅ Conexión a PostgreSQL
- ✅ Endpoints REST para GET y POST
- ✅ Validación de datos
- ✅ Gestión de errores
- ✅ CORS habilitado
- ✅ Variables de entorno para configuración
