# TODO API - Backend con Flask y PostgreSQL

Aplicación backend para gestión de usuarios y notas personales construida con Flask, SQLAlchemy y PostgreSQL.

## Características

- ✅ Registro y autenticación de usuarios
- ✅ CRUD de notas personales
- ✅ Validación de permisos mediante header `client-id`
- ✅ Base de datos PostgreSQL
- ✅ Contenedorización con Docker
- ✅ Documentación Swagger/OpenAPI interactiva
- ✅ CORS habilitado para cualquier dominio

## Tecnologías

- Python 3.11
- Flask 3.0.0
- Flask-CORS 4.0.0
- Flasgger (Swagger/OpenAPI)
- SQLAlchemy
- PostgreSQL 16
- Docker & Docker Compose

## Requisitos Previos

- Docker y Docker Compose instalados
- Python 3.11+ (si se ejecuta sin Docker)

## Instalación y Ejecución

### Con Docker (Recomendado)

1. Clonar el repositorio y navegar al directorio:
```bash
cd notas-backend
```

2. Iniciar los servicios:
```bash
docker-compose up --build
```

La aplicación estará disponible en `http://localhost:5000`

La documentación Swagger estará disponible en `http://localhost:5000/api/docs/`

### Sin Docker

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno (crear archivo `.env`):
```bash
DATABASE_URL=postgresql://usuario:password@localhost:5432/todo_db
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta
```

4. Ejecutar la aplicación:
```bash
python app.py
```

## Documentación de la API

### Swagger UI (Documentación Interactiva)

La API cuenta con documentación interactiva Swagger/OpenAPI donde puedes probar todos los endpoints directamente desde el navegador:

🔗 **Accede a Swagger UI:** `http://localhost:5000/api/docs/`

Desde Swagger UI puedes:
- Ver todos los endpoints disponibles organizados por tags
- Probar cada endpoint directamente desde el navegador
- Ver los esquemas de request/response
- Conocer los códigos de estado HTTP posibles
- Entender los parámetros requeridos y opcionales

### CORS

La API tiene CORS habilitado para permitir peticiones desde cualquier dominio. Puedes acceder a la API desde aplicaciones frontend hospedadas en cualquier URL.

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Respuesta exitosa (200):**
```json
{
  "status": "healthy"
}
```

---

#### 2. Registro de Usuario
```http
POST /register
Content-Type: application/json
```

**Body:**
```json
{
  "user": "username",
  "password": "password123",
  "name": "Nombre Completo"
}
```

**Respuesta exitosa (201):**
```json
{
  "message": "Usuario registrado exitosamente",
  "id": 1
}
```

**Errores posibles:**
- `400`: Faltan campos requeridos
- `409`: El usuario ya existe
- `500`: Error del servidor

---

#### 3. Login
```http
POST /login
Content-Type: application/json
```

**Body:**
```json
{
  "user": "username",
  "password": "password123"
}
```

**Respuesta exitosa (200):**
```json
{
  "message": "Login exitoso",
  "id": 1
}
```

**Errores posibles:**
- `400`: Faltan campos requeridos
- `401`: Usuario o contraseña incorrectos
- `500`: Error del servidor

---

#### 4. Crear Nota
```http
POST /notes
Content-Type: application/json
client-id: {user_id}
```

**Headers requeridos:**
- `client-id`: ID del usuario autenticado

**Body:**
```json
{
  "text": "Contenido de la nota"
}
```

**Respuesta exitosa (201):**
```json
{
  "message": "Nota creada exitosamente",
  "note": {
    "id": 1,
    "text": "Contenido de la nota",
    "user_id": 1,
    "created_at": "2024-12-11T10:30:00",
    "updated_at": "2024-12-11T10:30:00"
  }
}
```

**Errores posibles:**
- `400`: Falta el campo text o client-id inválido
- `401`: Header client-id no proporcionado
- `404`: Usuario no encontrado
- `500`: Error del servidor

---

#### 5. Obtener Todas las Notas
```http
GET /notes
client-id: {user_id}
```

**Headers requeridos:**
- `client-id`: ID del usuario autenticado

**Respuesta exitosa (200):**
```json
{
  "notes": [
    {
      "id": 1,
      "text": "Primera nota",
      "user_id": 1,
      "created_at": "2024-12-11T10:30:00",
      "updated_at": "2024-12-11T10:30:00"
    },
    {
      "id": 2,
      "text": "Segunda nota",
      "user_id": 1,
      "created_at": "2024-12-11T11:00:00",
      "updated_at": "2024-12-11T11:00:00"
    }
  ],
  "total": 2
}
```

**Errores posibles:**
- `401`: Header client-id no proporcionado
- `404`: Usuario no encontrado
- `500`: Error del servidor

---

#### 6. Obtener Nota por ID
```http
GET /notes/{note_id}
client-id: {user_id}
```

**Headers requeridos:**
- `client-id`: ID del usuario autenticado

**Respuesta exitosa (200):**
```json
{
  "note": {
    "id": 1,
    "text": "Contenido de la nota",
    "user_id": 1,
    "created_at": "2024-12-11T10:30:00",
    "updated_at": "2024-12-11T10:30:00"
  }
}
```

**Errores posibles:**
- `401`: Header client-id no proporcionado
- `403`: No tienes permiso para acceder a esta nota
- `404`: Nota o usuario no encontrado
- `500`: Error del servidor

---

## Ejemplos de Uso con cURL

### Registrar un usuario
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "user": "johndoe",
    "password": "secret123",
    "name": "John Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "user": "johndoe",
    "password": "secret123"
  }'
```

### Crear una nota
```bash
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -H "client-id: 1" \
  -d '{
    "text": "Mi primera nota"
  }'
```

### Obtener todas las notas
```bash
curl -X GET http://localhost:5000/notes \
  -H "client-id: 1"
```

### Obtener nota específica
```bash
curl -X GET http://localhost:5000/notes/1 \
  -H "client-id: 1"
```

## Estructura del Proyecto

```
notas-backend/
├── app.py                  # Aplicación principal Flask
├── models.py               # Modelos SQLAlchemy (User, Note)
├── requirements.txt        # Dependencias Python
├── Dockerfile              # Imagen Docker de la aplicación
├── docker-compose.yml      # Orquestación de servicios
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Este archivo
```

## Modelos de Base de Datos

### User
- `id`: Integer (PK)
- `name`: String(100)
- `user`: String(80) - único
- `password_hash`: String(255)

### Note
- `id`: Integer (PK)
- `text`: Text
- `user_id`: Integer (FK a User)
- `created_at`: DateTime
- `updated_at`: DateTime

## Seguridad

- Las contraseñas se almacenan hasheadas usando Werkzeug
- Validación de permisos mediante header `client-id`
- Las notas solo pueden ser accedidas por su propietario
- CORS habilitado para permitir acceso desde cualquier dominio (configurar según necesidades de producción)

## Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión PostgreSQL | `postgresql://todo_user:todo_password@db:5432/todo_db` |
| `FLASK_ENV` | Entorno de Flask | `development` |
| `SECRET_KEY` | Clave secreta para Flask | `dev-secret-key` |

## Detener los Servicios

```bash
docker-compose down
```

Para eliminar también los volúmenes (base de datos):
```bash
docker-compose down -v
```

## Desarrollo

Para acceder a la base de datos PostgreSQL directamente:
```bash
docker exec -it todo_postgres psql -U todo_user -d todo_db
```

## Licencia

MIT
