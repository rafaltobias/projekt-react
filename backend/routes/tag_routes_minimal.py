from flask import Blueprint

# Simple test
tag_bp = Blueprint('tag', __name__)

@tag_bp.route('/api/test')
def test():
    return "test"
