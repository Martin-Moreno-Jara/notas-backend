from flask import Flask
from flask_cors import CORS
from controllers.note_controller import note_bp
from config.database import init_db

app = Flask(__name__)
CORS(app)

# Configuración
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

# Inicializar base de datos
init_db()

# Registrar blueprints
app.register_blueprint(note_bp, url_prefix='/api/notes')

@app.route('/')
def home():
    return {'message': 'API de Notas - Backend funcionando'}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
