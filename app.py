import os
from functools import wraps

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, jsonify, request
from flask_cors import CORS

from models import Note, User, db

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

CORS(
    app,
    resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}},
)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/",
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "TODO API - Gestión de Usuarios y Notas",
        "description": "API REST para gestión de usuarios y notas personales con autenticación",
        "version": "1.0.0",
        "contact": {"name": "API Support", "email": "support@example.com"},
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"],
    "securityDefinitions": {
        "ClientID": {
            "type": "apiKey",
            "name": "client-id",
            "in": "header",
            "description": "ID del usuario autenticado",
        }
    },
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

db.init_app(app)


def validate_client_id(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_id = request.headers.get("client-id")

        if not client_id:
            return jsonify({"error": "Header client-id es requerido"}), 401

        try:
            client_id = int(client_id)
        except ValueError:
            return jsonify({"error": "Header client-id debe ser un número válido"}), 400

        user = User.query.get(client_id)
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        request.current_user_id = client_id
        return f(*args, **kwargs)

    return decorated_function


@app.route("/register", methods=["POST"])
def register():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        description: Datos del usuario a registrar
        schema:
          type: object
          required:
            - user
            - password
            - name
          properties:
            user:
              type: string
              example: "johndoe"
              description: Nombre de usuario único
            password:
              type: string
              example: "secret123"
              description: Contraseña del usuario
            name:
              type: string
              example: "John Doe"
              description: Nombre completo del usuario
    responses:
      201:
        description: Usuario registrado exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Usuario registrado exitosamente"
            id:
              type: integer
              example: 1
              description: ID del usuario creado
      400:
        description: Datos inválidos o incompletos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Faltan campos requeridos: user, password, name"
      409:
        description: El usuario ya existe
        schema:
          type: object
          properties:
            error:
              type: string
              example: "El usuario ya existe"
      500:
        description: Error del servidor
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        user = data.get("user")
        password = data.get("password")
        name = data.get("name")

        if not user or not password or not name:
            return (
                jsonify({"error": "Faltan campos requeridos: user, password, name"}),
                400,
            )

        existing_user = User.query.filter_by(user=user).first()
        if existing_user:
            return jsonify({"error": "El usuario ya existe"}), 409

        new_user = User(user=user, name=name)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return (
            jsonify({"message": "Usuario registrado exitosamente", "id": new_user.id}),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al registrar usuario: {str(e)}"}), 500


@app.route("/login", methods=["POST"])
def login():
    """
    Autenticar un usuario
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        description: Credenciales del usuario
        schema:
          type: object
          required:
            - user
            - password
          properties:
            user:
              type: string
              example: "johndoe"
              description: Nombre de usuario
            password:
              type: string
              example: "secret123"
              description: Contraseña del usuario
    responses:
      200:
        description: Login exitoso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Login exitoso"
            user_id:
              type: integer
              example: 1
              description: ID del usuario autenticado
            name:
              type: string
              example: "John Doe"
              description: Nombre completo del usuario
      400:
        description: Datos inválidos o incompletos
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Faltan campos requeridos: user, password"
      401:
        description: Credenciales incorrectas
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Usuario o contraseña incorrectos"
      500:
        description: Error del servidor
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        user = data.get("user")
        password = data.get("password")

        if not user or not password:
            return jsonify({"error": "Faltan campos requeridos: user, password"}), 400

        existing_user = User.query.filter_by(user=user).first()

        if not existing_user or not existing_user.check_password(password):
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

        return (
            jsonify(
                {
                    "message": "Login exitoso",
                    "user_id": existing_user.id,
                    "name": existing_user.name,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": f"Error al iniciar sesión: {str(e)}"}), 500


@app.route("/health", methods=["GET"])
def health():
    """
    Verificar el estado de la API
    ---
    tags:
      - Salud
    responses:
      200:
        description: API funcionando correctamente
        schema:
          type: object
          properties:
            status:
              type: string
              example: "healthy"
    """
    return jsonify({"status": "healthy"}), 200


@app.route("/notes", methods=["POST"])
@validate_client_id
def create_note():
    """
    Crear una nueva nota
    ---
    tags:
      - Notas
    security:
      - ClientID: []
    parameters:
      - in: header
        name: client-id
        type: integer
        required: true
        description: ID del usuario autenticado
        example: 1
      - in: body
        name: body
        required: true
        description: Contenido de la nota
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              example: "Mi primera nota"
              description: Contenido de la nota
    responses:
      201:
        description: Nota creada exitosamente
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Nota creada exitosamente"
            note:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                text:
                  type: string
                  example: "Mi primera nota"
                user_id:
                  type: integer
                  example: 1
                created_at:
                  type: string
                  example: "2024-12-11T10:30:00"
                updated_at:
                  type: string
                  example: "2024-12-11T10:30:00"
      400:
        description: Datos inválidos o header client-id inválido
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Header client-id no proporcionado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Header client-id es requerido"
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Usuario no encontrado"
      500:
        description: Error del servidor
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        text = data.get("text")

        if not text:
            return jsonify({"error": "El campo text es requerido"}), 400

        new_note = Note(text=text, user_id=request.current_user_id)

        db.session.add(new_note)
        db.session.commit()

        return (
            jsonify(
                {"message": "Nota creada exitosamente", "note": new_note.to_dict()}
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear nota: {str(e)}"}), 500


@app.route("/notes", methods=["GET"])
@validate_client_id
def get_all_notes():
    """
    Obtener todas las notas del usuario autenticado
    ---
    tags:
      - Notas
    security:
      - ClientID: []
    parameters:
      - in: header
        name: client-id
        type: integer
        required: true
        description: ID del usuario autenticado
        example: 1
    responses:
      200:
        description: Lista de notas obtenida exitosamente
        schema:
          type: object
          properties:
            notes:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  text:
                    type: string
                    example: "Mi primera nota"
                  user_id:
                    type: integer
                    example: 1
                  created_at:
                    type: string
                    example: "2024-12-11T10:30:00"
                  updated_at:
                    type: string
                    example: "2024-12-11T10:30:00"
            total:
              type: integer
              example: 5
              description: Número total de notas
      400:
        description: Header client-id inválido
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Header client-id no proporcionado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Header client-id es requerido"
      404:
        description: Usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Usuario no encontrado"
      500:
        description: Error del servidor
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        notes = Note.query.filter_by(user_id=request.current_user_id).all()

        return (
            jsonify({"notes": [note.to_dict() for note in notes], "total": len(notes)}),
            200,
        )

    except Exception as e:
        return jsonify({"error": f"Error al obtener notas: {str(e)}"}), 500


@app.route("/notes/<int:note_id>", methods=["GET"])
@validate_client_id
def get_note_by_id(note_id):
    """
    Obtener una nota específica por ID
    ---
    tags:
      - Notas
    security:
      - ClientID: []
    parameters:
      - in: header
        name: client-id
        type: integer
        required: true
        description: ID del usuario autenticado
        example: 1
      - in: path
        name: note_id
        type: integer
        required: true
        description: ID de la nota a obtener
        example: 1
    responses:
      200:
        description: Nota obtenida exitosamente
        schema:
          type: object
          properties:
            note:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                text:
                  type: string
                  example: "Mi primera nota"
                user_id:
                  type: integer
                  example: 1
                created_at:
                  type: string
                  example: "2024-12-11T10:30:00"
                updated_at:
                  type: string
                  example: "2024-12-11T10:30:00"
      400:
        description: Header client-id inválido
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Header client-id no proporcionado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Header client-id es requerido"
      403:
        description: No tienes permiso para acceder a esta nota
        schema:
          type: object
          properties:
            error:
              type: string
              example: "No tienes permiso para acceder a esta nota"
      404:
        description: Nota o usuario no encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Nota no encontrada"
      500:
        description: Error del servidor
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        note = Note.query.get(note_id)

        if not note:
            return jsonify({"error": "Nota no encontrada"}), 404

        if note.user_id != request.current_user_id:
            return jsonify({"error": "No tienes permiso para acceder a esta nota"}), 403

        return jsonify({"note": note.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": f"Error al obtener nota: {str(e)}"}), 500


def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
