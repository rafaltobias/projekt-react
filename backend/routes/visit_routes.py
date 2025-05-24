from flask import Blueprint, request, jsonify
from models.visit_model import add_visit, update_exit_pages
import requests

visit_bp = Blueprint('visit', __name__)

def get_location_from_ip(ip_address):
    """Get location information from IP address using a free IP geolocation service"""
    try:
        # Use a free IP geolocation service (you can replace with your preferred service)
        response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    'country': data.get('country'),
                    'city': data.get('city'),
                    'region': data.get('regionName')
                }
    except Exception as e:
        print(f"Error getting location for IP {ip_address}: {e}")
    
    return {'country': None, 'city': None, 'region': None}

@visit_bp.route('/api/track', methods=['POST'])
def track_visit():
    data = request.get_json()
    
    if not data or 'page_url' not in data:
        return jsonify({'error': 'page_url is required'}), 400
    
    page_url = data.get('page_url')
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    referrer = data.get('referrer') or request.headers.get('Referer')
    browser = data.get('browser')
    os = data.get('os')
    device = data.get('device')
    country = data.get('country')
    session_id = data.get('session_id')
    is_entry_page = data.get('is_entry_page', False)
    is_exit_page = data.get('is_exit_page', False)
    event_name = data.get('event_name')
    event_data = data.get('event_data')
    
    # Get location from IP if not provided
    if not country and ip_address and ip_address != '127.0.0.1':
        location_data = get_location_from_ip(ip_address)
        country = location_data['country']
    
    try:
        visit_id = add_visit(
            page_url, ip_address, user_agent, referrer, 
            browser, os, device, country, 
            session_id, is_entry_page, is_exit_page,
            event_name, event_data
        )
        
        # If this is a new page visit (not an event), update previous visits in the session
        if session_id and not event_name:
            update_exit_pages(session_id, visit_id)
        
        return jsonify({
            'success': True,
            'visit_id': visit_id,
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
