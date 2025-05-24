from flask import Blueprint, request, jsonify
from models.visit_model import add_visit

visit_bp = Blueprint('visit', __name__)

@visit_bp.route('/api/track', methods=['POST'])
def track_visit():
    data = request.get_json()
    
    if not data or 'page_url' not in data:
        return jsonify({'error': 'page_url is required'}), 400
    
    page_url = data.get('page_url')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    referrer = request.headers.get('Referer')
    browser = data.get('browser')
    os = data.get('os')
    device = data.get('device')
    country = data.get('country')
    session_id = data.get('session_id')
    is_entry_page = data.get('is_entry_page', False)
    is_exit_page = data.get('is_exit_page', False)
    
    try:
        visit_id = add_visit(
            page_url, ip_address, user_agent, referrer, 
            browser, os, device, country, 
            session_id, is_entry_page, is_exit_page
        )
        return jsonify({
            'success': True,
            'visit_id': visit_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
