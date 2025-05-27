from flask import Blueprint, request, jsonify
from flask_restx import Namespace, fields
from pydantic import ValidationError
from models.tag_model import create_tag, get_all_tags, get_tag_by_id, delete_tag
from schemas.tag_schemas import TagRequest, TagResponse, TagCreateResponse, TagsListResponse
from schemas.base_schemas import BaseResponse, ErrorResponse
from utils.validation import (
    validate_request_data, map_db_result_to_schema, map_db_results_to_schemas,
    create_success_response, create_error_response
)

tag_bp = Blueprint('tag', __name__)

# Create API namespace for this blueprint
api = Namespace('tags', description='Tag management endpoints')

# Define Swagger models for documentation
tag_model = api.model('Tag', {
    'name': fields.String(required=True, description='Tag name'),
    'description': fields.String(description='Tag description'), 
    'type': fields.String(description='Tag type'),
    'trigger': fields.String(description='Tag trigger condition'),
    'config': fields.Raw(description='Tag configuration')
})

@tag_bp.route('/api/tags', methods=['POST'])
@api.expect(tag_model)
@api.response(201, 'Tag created successfully')
@api.response(400, 'Validation error')
@api.response(500, 'Internal server error')
def add_tag():
    """Create a new tag"""
    try:
        data = request.get_json()
        if not data:
            return create_error_response('No JSON data provided')
        
        # Validate request data using Pydantic schema
        validation_result = validate_request_data(TagRequest, data)
        if isinstance(validation_result, tuple):  # Error response
            return validation_result
        
        tag_request = validation_result
        
        # Create the tag
        tag_id = create_tag(
            tag_request.name,
            tag_request.description,
            tag_request.type,
            tag_request.trigger,
            tag_request.config
        )
        
        # Create response using schema
        response = TagCreateResponse(
            success=True,
            tag_id=tag_id
        )
        
        return jsonify(response.model_dump()), 201
        
    except Exception as e:
        return create_error_response(f'Failed to create tag: {str(e)}', status_code=500)


@tag_bp.route('/api/tags', methods=['GET'])
@api.response(200, 'Tags retrieved successfully')
@api.response(500, 'Internal server error')
def get_tags():
    """Get all tags"""
    try:
        db_tags = get_all_tags()
        
        # Map database results to response schemas
        tags = map_db_results_to_schemas(db_tags or [], TagResponse)
        
        # Create response using schema
        response = TagsListResponse(tags=tags)
        
        return jsonify(response.model_dump())
        
    except Exception as e:
        return create_error_response(f'Failed to retrieve tags: {str(e)}', status_code=500)

@tag_bp.route('/api/tags/<int:id>', methods=['GET'])
@api.response(200, 'Tag retrieved successfully')
@api.response(404, 'Tag not found')
@api.response(500, 'Internal server error')
def get_tag(id):
    """Get a specific tag by ID"""
    try:
        db_tag = get_tag_by_id(id)
        
        if not db_tag:
            return create_error_response('Tag not found', status_code=404)
        
        # Map database result to response schema
        tag = map_db_result_to_schema(db_tag, TagResponse)
        
        return jsonify(tag.model_dump())
        
    except Exception as e:
        return create_error_response(f'Failed to retrieve tag: {str(e)}', status_code=500)


@tag_bp.route('/api/tags/<int:id>', methods=['DELETE'])
@api.response(200, 'Tag deleted successfully')
@api.response(404, 'Tag not found')
@api.response(500, 'Internal server error')
def remove_tag(id):
    """Delete a specific tag by ID"""
    try:
        success = delete_tag(id)
        
        if not success:
            return create_error_response('Tag not found', status_code=404)
        
        # Create success response
        response = BaseResponse(success=True, message='Tag deleted successfully')
        
        return jsonify(response.model_dump())
        
    except Exception as e:
        return create_error_response(f'Failed to delete tag: {str(e)}', status_code=500)
