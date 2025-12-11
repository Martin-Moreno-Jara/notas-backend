import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'notas_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '5432')
}

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def init_db():
    """Inicializa la base de datos creando las tablas necesarias"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Crear tabla de notas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    user_id VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Crear índice para mejorar las búsquedas por usuario
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_user_id ON notes(user_id)
            ''')
            
            conn.commit()
            cursor.close()
            print("Base de datos inicializada correctamente")
        except Exception as e:
            print(f"Error inicializando la base de datos: {e}")
        finally:
            conn.close()
