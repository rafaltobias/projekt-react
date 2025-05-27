from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError
from models.visit_model import add_visit, update_exit_pages
from schemas.visit_schemas import VisitRequest, VisitResponse, VisitCreateResponse
from schemas.base_schemas import ErrorResponse
from utils.validation import (
    validate_request_data, create_success_response, create_error_response
)
import requests

visit_bp = Blueprint('visit', __name__)

# Create API namespace for this blueprint
api = Namespace('visits', description='Visit tracking endpoints')

# Define Swagger models for documentation
visit_model = api.model('Visit', {
    'page_url': fields.String(required=True, description='Page URL'),
    'referrer': fields.String(description='Referrer URL'),
    'browser': fields.String(description='Browser name'),
    'os': fields.String(description='Operating system'),
    'device': fields.String(description='Device type'),
    'country': fields.String(description='Country code'),
    'session_id': fields.String(description='Session identifier'),
    'is_entry_page': fields.Boolean(description='Is entry page'),
    'is_exit_page': fields.Boolean(description='Is exit page'),
    'event_name': fields.String(description='Custom event name'),
    'event_data': fields.Raw(description='Custom event data')
})

def get_location_from_ip(ip_address):
    """Get location information from IP address using a free IP geolocation service"""
    try:
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
@api.expect(visit_model)
@api.response(201, 'Visit tracked successfully')
@api.response(400, 'Validation error')
@api.response(500, 'Internal server error')
def track_visit():
    """Track a visit to a page"""
    try:
        data = request.get_json()
        if not data:
            return create_error_response('No JSON data provided')
        
        # Validate request data using Pydantic schema
        validation_result = validate_request_data(VisitRequest, data)
        if isinstance(validation_result, tuple):  # Error response
            return validation_result
        
        visit_request = validation_result
        
        # Add IP address and user agent from request headers
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        
        # Use referrer from request data or headers
        referrer = visit_request.referrer or request.headers.get('Referer')
        
        # Get location from IP if not provided
        country = visit_request.country
        if not country and ip_address and ip_address != '127.0.0.1':
            location_data = get_location_from_ip(ip_address)
            country = location_data.get('country') if location_data else None
        
        # Add the visit
        visit_id = add_visit(
            visit_request.page_url, 
            ip_address, 
            user_agent, 
            referrer, 
            visit_request.browser, 
            visit_request.os, 
            visit_request.device, 
            country, 
            visit_request.session_id, 
            visit_request.is_entry_page, 
            visit_request.is_exit_page,
            visit_request.event_name, 
            visit_request.event_data
        )
        
        # If this is a new page visit (not an event), update previous visits in the session
        if visit_request.session_id and not visit_request.event_name:
            update_exit_pages(visit_request.session_id, visit_id)
        
        # Create response using schema
        response = VisitCreateResponse(
            success=True,
            visit_id=visit_id,
            session_id=visit_request.session_id
        )
        
        return jsonify(response.model_dump()), 201
        
    except Exception as e:
        return create_error_response(f'Failed to track visit: {str(e)}', status_code=500)
