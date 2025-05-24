from flask import Blueprint, request, jsonify, send_from_directory
from models.tracking_model import (
    add_tracking_event, get_tracking_events, get_page_views, 
    get_custom_events, get_session_data, get_session_analytics, 
    get_tracking_stats, update_exit_pages, get_real_time_stats
)
import os

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/api/track', methods=['POST'])
def track_event():
    """Track a page view or custom event"""
    try:
        data = request.get_json()
        
        if not data or 'page_url' not in data or 'session_id' not in data:
            return jsonify({'error': 'page_url and session_id are required'}), 400
        
        # Extract data from request
        session_id = data.get('session_id')
        page_url = data.get('page_url')
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        referrer = data.get('referrer') or request.headers.get('Referer')
        browser = data.get('browser')
        os = data.get('os')
        device = data.get('device')
        country = data.get('country')
        city = data.get('city')
        is_entry_page = data.get('is_entry_page', False)
        is_exit_page = data.get('is_exit_page', False)
        event_name = data.get('event_name')
        event_data = data.get('event_data')
        
        # Add the tracking event
        result = add_tracking_event(
            session_id=session_id,
            page_url=page_url,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
            browser=browser,
            os=os,
            device=device,
            country=country,
            city=city,
            is_entry_page=is_entry_page,
            is_exit_page=is_exit_page,
            event_name=event_name,
            event_data=event_data
        )
        
        if result:
            # Update previous events in session to not be exit pages
            if not is_exit_page:
                update_exit_pages(session_id, result['id'])
            
            return jsonify({
                'success': True,
                'event_id': result['id'],
                'timestamp': result['timestamp'].isoformat()
            })
        else:
            return jsonify({'error': 'Failed to track event'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tracking_bp.route('/api/tracking/events', methods=['GET'])
def get_events():
    """Get tracking events with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        event_type = request.args.get('type', 'all')  # all, page_views, custom_events
        
        offset = (page - 1) * per_page
        
        if event_type == 'page_views':
            events = get_page_views(limit=per_page, offset=offset)
        elif event_type == 'custom_events':
            events = get_custom_events(limit=per_page, offset=offset)
        else:
            events = get_tracking_events(limit=per_page, offset=offset)
        
        return jsonify({
            'events': events,
            'page': page,
            'per_page': per_page,
            'type': event_type
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tracking_bp.route('/api/tracking/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get all events for a specific session"""
    try:
        events = get_session_data(session_id)
        analytics = get_session_analytics(session_id)
        
        return jsonify({
            'session_id': session_id,
            'events': events,
            'analytics': analytics[0] if analytics else None
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tracking_bp.route('/api/tracking/sessions', methods=['GET'])
def get_sessions():
    """Get session analytics"""
    try:
        sessions = get_session_analytics()
        return jsonify({
            'sessions': sessions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tracking_bp.route('/api/tracking/stats', methods=['GET'])
def get_stats():
    """Get tracking statistics"""
    try:
        days = request.args.get('days', 30, type=int)
        stats = get_tracking_stats(days)
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tracking_bp.route('/api/tracking/realtime', methods=['GET'])
def get_realtime():
    """Get real-time tracking statistics"""
    try:
        stats = get_real_time_stats()
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve tracking script
@tracking_bp.route('/static/tracker.js', methods=['GET'])
def serve_tracker_js():
    """Serve the tracking script"""
    try:
        # Get the path to the frontend static files
        frontend_static_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            '..', 'frontend', 'src', 'static'
        )
        return send_from_directory(frontend_static_path, 'tracker.js')
    except Exception as e:
        return jsonify({'error': 'Tracker script not found'}), 404

@tracking_bp.route('/static/tracker.min.js', methods=['GET'])
def serve_tracker_min_js():
    """Serve the minified tracking script"""
    try:
        # Get the path to the frontend static files
        frontend_static_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            '..', 'frontend', 'src', 'static'
        )
        return send_from_directory(frontend_static_path, 'tracker.min.js')
    except Exception as e:
        return jsonify({'error': 'Tracker script not found'}), 404

# Serve tracking example page
@tracking_bp.route('/tracking-example', methods=['GET'])
def serve_tracking_example():
    """Serve the tracking example page"""
    try:
        # Get the path to the frontend public files
        frontend_public_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            '..', 'frontend', 'public'
        )
        return send_from_directory(frontend_public_path, 'tracking-example.html')
    except Exception as e:
        return jsonify({'error': 'Example page not found'}), 404
