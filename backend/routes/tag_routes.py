from flask import Blueprint, request, jsonify
from models.tag_model import create_tag, get_all_tags, get_tag_by_id, delete_tag

tag_bp = Blueprint('tag', __name__)

@tag_bp.route('/api/tags', methods=['POST'])
def add_tag():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Tag name is required'}), 400
    
    name = data.get('name')
    description = data.get('description')
    
    try:
        tag_id = create_tag(name, description)
        return jsonify({
            'success': True,
            'tag_id': tag_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tag_bp.route('/api/tags', methods=['GET'])
def get_tags():
    try:
        tags = get_all_tags()
        return jsonify(tags)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tag_bp.route('/api/tags/<int:id>', methods=['GET'])
def get_tag(id):
    try:
        tag = get_tag_by_id(id)
        if tag:
            return jsonify(tag)
        return jsonify({'error': 'Tag not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tag_bp.route('/api/tags/<int:id>', methods=['DELETE'])
def remove_tag(id):
    try:
        success = delete_tag(id)
        if success:
            return jsonify({'success': True})
        return jsonify({'error': 'Tag not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
