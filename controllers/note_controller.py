from flask import Blueprint, request, jsonify
from models.note import Note

note_bp = Blueprint('notes', __name__)

@note_bp.route('/<user_id>', methods=['GET'])
def get_notes(user_id):
    """
    GET /api/notes/<user_id>
    Obtiene todas las notas de un usuario específico
    """
    try:
        notes = Note.get_all_by_user(user_id)
        notes_dict = [note.to_dict() for note in notes]
        
        return jsonify({
            'success': True,
            'data': notes_dict,
            'count': len(notes_dict)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@note_bp.route('/', methods=['POST'])
def create_note():
    """
    POST /api/notes/
    Crea una nueva nota
    Body JSON:
    {
        "title": "Título de la nota",
        "content": "Contenido de la nota",
        "user_id": "id_del_usuario"
    }
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        user_id = data.get('user_id', '').strip()
        
        if not title:
            return jsonify({
                'success': False,
                'error': 'El título es requerido'
            }), 400
        
        if not content:
            return jsonify({
                'success': False,
                'error': 'El contenido es requerido'
            }), 400
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'El user_id es requerido'
            }), 400
        
        # Crear y guardar la nota
        note = Note(title=title, content=content, user_id=user_id)
        saved_note = note.save()
        
        if saved_note:
            return jsonify({
                'success': True,
                'data': saved_note.to_dict(),
                'message': 'Nota creada exitosamente'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Error al guardar la nota'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
