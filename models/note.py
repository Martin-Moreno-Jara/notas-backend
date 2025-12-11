from datetime import datetime
from config.database import get_db_connection

class Note:
    def __init__(self, id=None, title='', content='', user_id='', created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.content = content
        self.user_id = user_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        """Convierte el objeto Note a un diccionario"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }
    
    @staticmethod
    def get_all_by_user(user_id):
        """Obtiene todas las notas de un usuario específico"""
        conn = get_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM notes WHERE user_id = %s ORDER BY created_at DESC',
                (user_id,)
            )
            rows = cursor.fetchall()
            cursor.close()
            
            notes = []
            for row in rows:
                note = Note(
                    id=row['id'],
                    title=row['title'],
                    content=row['content'],
                    user_id=row['user_id'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                notes.append(note)
            
            return notes
        except Exception as e:
            print(f"Error obteniendo notas: {e}")
            return []
        finally:
            conn.close()
    
    def save(self):
        """Guarda una nueva nota en la base de datos"""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO notes (title, content, user_id, created_at, updated_at) 
                   VALUES (%s, %s, %s, %s, %s) RETURNING id''',
                (self.title, self.content, self.user_id, self.created_at, self.updated_at)
            )
            self.id = cursor.fetchone()['id']
            conn.commit()
            cursor.close()
            return self
        except Exception as e:
            print(f"Error guardando nota: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(note_id):
        """Obtiene una nota por su ID"""
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM notes WHERE id = %s', (note_id,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return Note(
                    id=row['id'],
                    title=row['title'],
                    content=row['content'],
                    user_id=row['user_id'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None
        except Exception as e:
            print(f"Error obteniendo nota: {e}")
            return None
        finally:
            conn.close()
