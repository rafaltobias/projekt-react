from flask import Blueprint, request, jsonify, send_from_directory
from flask_restx import Namespace, Resource, fields
from services.tracking_service import TrackingService
from services.request_processing_service import RequestProcessingService
from services.file_serving_service import FileServingService
from schemas.tracking_schemas import (
    TrackingEventRequest, TrackingEventResponse, TrackingEventCreateResponse,
    TrackingEventsResponse, SessionDataResponse, SessionAnalyticsResponse,
    TrackingStatsResponse, RealtimeStatsResponse
)
from schemas.base_schemas import PaginationParams, DateRangeParams, ErrorResponse
from utils.validation import (
    validate_request_data, create_success_response, create_error_response
)
import os

tracking_bp = Blueprint('tracking', __name__)

# Create API namespace for this blueprint
api = Namespace('tracking', description='Event tracking endpoints')

# Define Swagger models for documentation
tracking_event_model = api.model('TrackingEvent', {
    'session_id': fields.String(required=True, description='Session ID'),
    'page_url': fields.String(required=True, description='Page URL'),
    'referrer': fields.String(description='Referrer URL'),
    'browser': fields.String(description='Browser name'),
    'os': fields.String(description='Operating system'),
    'device': fields.String(description='Device type'),
    'country': fields.String(description='Country code'),
    'city': fields.String(description='City name'),
    'is_entry_page': fields.Boolean(description='Is entry page'),
    'is_exit_page': fields.Boolean(description='Is exit page'),
    'event_name': fields.String(description='Custom event name'),
    })

@tracking_bp.route('/api/track', methods=['POST'])
@api.expect(tracking_event_model)
@api.response(201, 'Event tracked successfully')
@api.response(400, 'Validation error')
@api.response(500, 'Internal server error')
def track_event():
    """Track a page view or custom event"""
    try:
        data = request.get_json()
        if not data:
            return create_error_response('No JSON data provided')
        
        # Validate request data using Pydantic schema
        validation_result = validate_request_data(TrackingEventRequest, data)
        if isinstance(validation_result, tuple):  # Error response
            return validation_result
        
        tracking_request = validation_result
        
        # Extract request metadata using service
        request_metadata = RequestProcessingService.extract_request_metadata(request)
        
        # Process tracking event using business logic service
        result = TrackingService.process_tracking_event(
            tracking_request.model_dump(),
            request_metadata
        )
        
        if result:
            # Create response using schema
            response = TrackingEventCreateResponse(
                success=True,
                event_id=result['id'],
                timestamp=result['timestamp']
            )
            return jsonify(response.model_dump()), 201
        else:
            return create_error_response('Failed to track event', status_code=500)
            
    except Exception as e:
        return create_error_response(f'Internal server error: {str(e)}', status_code=500)

@tracking_bp.route('/api/tracking/events', methods=['GET'])
@api.response(200, 'Events retrieved successfully')
@api.response(400, 'Invalid parameters')
@api.response(500, 'Internal server error')
def get_events():
    """Get tracking events with pagination"""
    try:
        # Parse query parameters using Pydantic
        params_data = {
            'page': request.args.get('page', 1, type=int),
            'per_page': request.args.get('per_page', 50, type=int)
        }
        
        # Validate pagination parameters
        validation_result = validate_request_data(PaginationParams, params_data)
        if isinstance(validation_result, tuple):  # Error response
            return validation_result
        
        pagination = validation_result
        event_type = request.args.get('type', 'all')  # all, page_views, custom_events
        
        offset = (pagination.page - 1) * pagination.per_page
          # Get events based on type using service
        if event_type == 'page_views':
            db_events = TrackingService.get_page_views(limit=pagination.per_page, offset=offset)
        elif event_type == 'custom_events':
            db_events = TrackingService.get_custom_events(limit=pagination.per_page, offset=offset)
        else:
            db_events = TrackingService.get_tracking_events(limit=pagination.per_page, offset=offset)
          # Map database results to response schemas
        events = []
        for event in db_events:
            # Convert to dict if it's not already (handles both ORM objects and dicts)
            event_dict = event if isinstance(event, dict) else event
            events.append(event_dict)
          # Create response using schema
        response = TrackingEventsResponse(
            events=events,
            page=pagination.page,
            per_page=pagination.per_page,
            type=event_type,
            total=len(events),  # This should ideally come from a count query
            has_next=len(events) == pagination.per_page
        )
        
        return jsonify(response.model_dump())
        
    except Exception as e:
        return create_error_response(f'Failed to retrieve events: {str(e)}', status_code=500)

@tracking_bp.route('/api/tracking/session/<session_id>', methods=['GET'])
@api.response(200, 'Session data retrieved successfully')
@api.response(404, 'Session not found')
@api.response(500, 'Internal server error')
def get_session(session_id):
    """Get all events for a specific session"""
    try:        # Get session data from service
        session_data = TrackingService.get_session_data(session_id)
        
        if not session_data:
            return create_error_response('Session not found', status_code=404)
          # Map events to response schemas - events are already dicts from service
        events = session_data.get('events', [])
        
        # Create response using schema
        response = SessionDataResponse(
            session_id=session_id,
            events=events,
            total_events=len(events),        duration=session_data.get('duration'),
            entry_page=session_data.get('entry_page'),
            exit_page=session_data.get('exit_page')
        )
        
        return jsonify(response.model_dump())
        
    except Exception as e:
        return create_error_response(f'Failed to retrieve session data: {str(e)}', status_code=500)


@tracking_bp.route('/api/tracking/sessions', methods=['GET'])
@api.response(200, 'Session analytics retrieved successfully')
@api.response(500, 'Internal server error')
def get_sessions():
    """Get session analytics"""
    try:
        sessions_data = TrackingService.get_session_analytics()
        
        # Create response using schema
        response = SessionAnalyticsResponse(
            total_sessions=sessions_data.get('total_sessions', 0),
            average_session_duration=sessions_data.get('average_session_duration'),
            bounce_rate=sessions_data.get('bounce_rate'),
            top_entry_pages=sessions_data.get('top_entry_pages', []),
            top_exit_pages=sessions_data.get('top_exit_pages', [])
        )
        
        return jsonify(response.model_dump())
        
    except Exception as e:
        return create_error_response(f'Failed to retrieve session analytics: {str(e)}', status_code=500)


@tracking_bp.route('/api/tracking/stats', methods=['GET'])
@api.response(200, 'Tracking statistics retrieved successfully')
@api.response(400, 'Invalid parameters')
@api.response(500, 'Internal server error')
def get_stats():
    """Get tracking statistics"""
    try:
        # Parse and validate query parameters
        params_data = {
            'days': request.args.get('days', 30, type=int)
        }
        
        validation_result = validate_request_data(DateRangeParams, params_data)
        if isinstance(validation_result, tuple):  # Error response
            return validation_result
        date_params = validation_result
        stats_data = TrackingService.get_tracking_stats(date_params.days)
        
        # Create response using schema
        response = TrackingStatsResponse(
            total_page_views=stats_data.get('total_page_views', 0),
            total_custom_events=stats_data.get('total_custom_events', 0),
            unique_sessions=stats_data.get('unique_sessions', 0),
            top_pages=stats_data.get('top_pages', []),
            top_events=stats_data.get('top_events', []),
            hourly_stats=stats_data.get('hourly_stats', []),
            daily_stats=stats_data.get('daily_stats', [])
        )
        
        return jsonify(response.model_dump())
        
    except Exception as e:
        return create_error_response(f'Failed to retrieve tracking statistics: {str(e)}', status_code=500)

@tracking_bp.route('/api/tracking/realtime', methods=['GET'])
@api.response(200, 'Real-time statistics retrieved successfully')
@api.response(500, 'Internal server error')
def get_realtime():
    """Get real-time tracking statistics"""
    try:
        stats_data = TrackingService.get_realtime_stats()
        
        # Map recent events - they're already dicts from service
        recent_events = stats_data.get('recent_events', [])
        
        # Create response using schema
        response = RealtimeStatsResponse(
            active_sessions=stats_data.get('active_sessions', 0),
            page_views_last_hour=stats_data.get('page_views_last_hour', 0),
            top_pages_today=stats_data.get('top_pages_today', []),
            recent_events=recent_events
        )
        
        return jsonify(response.model_dump())
        
    except Exception as e:
        return create_error_response(f'Failed to retrieve real-time statistics: {str(e)}', status_code=500)

# Serve tracking script
@tracking_bp.route('/static/tracker.js', methods=['GET'])
def serve_tracker_js():
    """Serve the tracking script"""
    try:
        static_path, filename = FileServingService.get_tracker_script_info('regular')
        
        if not FileServingService.validate_file_exists(static_path, filename):
            return jsonify({'error': 'Tracker script not found'}), 404
            
        return send_from_directory(static_path, filename)
    except Exception as e:
        return jsonify({'error': 'Tracker script not found'}), 404

@tracking_bp.route('/static/tracker.min.js', methods=['GET'])
def serve_tracker_min_js():
    """Serve the minified tracking script"""
    try:
        static_path, filename = FileServingService.get_tracker_script_info('minified')
        
        if not FileServingService.validate_file_exists(static_path, filename):
            return jsonify({'error': 'Tracker script not found'}), 404
            
        return send_from_directory(static_path, filename)
    except Exception as e:
        return jsonify({'error': 'Tracker script not found'}), 404

# Serve tracking example page
@tracking_bp.route('/tracking-example', methods=['GET'])
def serve_tracking_example():
    """Serve the tracking example page"""
    try:
        public_path = FileServingService.get_frontend_public_path()
        filename = 'tracking-example.html'
        
        if not FileServingService.validate_file_exists(public_path, filename):
            return jsonify({'error': 'Example page not found'}), 404
            
        return send_from_directory(public_path, filename)
    except Exception as e:
        return jsonify({'error': 'Example page not found'}), 404
