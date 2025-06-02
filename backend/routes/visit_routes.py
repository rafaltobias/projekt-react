from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError
from services.visit_service import VisitService
from services.request_processing_service import RequestProcessingService
from schemas.visit_schemas import VisitRequest, VisitResponse, VisitCreateResponse
from schemas.base_schemas import ErrorResponse
from utils.validation import (
    validate_request_data, create_success_response, create_error_response
)
import logging

logger = logging.getLogger(__name__)

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
    'event_name': fields.String(description='Custom event name'),    'event_data': fields.Raw(description='Custom event data')
})

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
        
        # Extract request metadata using service
        request_metadata = RequestProcessingService.extract_request_metadata(request)
        
        # Process visit tracking using business logic service
        visit_id = VisitService.process_visit_tracking(
            visit_request.model_dump(),
            request_metadata
        )
        
        if not visit_id:
            return create_error_response('Failed to create visit record', status_code=500)
        
        # Create response using schema
        response = VisitCreateResponse(
            success=True,
            visit_id=visit_id,
            session_id=visit_request.session_id
        )
        
        return jsonify(response.model_dump()), 201
        
    except Exception as e:
        logger.error(f"Failed to track visit: {str(e)}")
        return create_error_response(f'Failed to track visit: {str(e)}', status_code=500)
