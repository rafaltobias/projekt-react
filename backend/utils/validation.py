"""
Utility functions for data validation and mapping
"""
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, ValidationError
from flask import jsonify
import json
from datetime import datetime


def validate_request_data(schema_class: BaseModel, data: Dict[str, Any]) -> Union[BaseModel, tuple]:
    """
    Validate request data against a Pydantic schema
    
    Args:
        schema_class: Pydantic model class to validate against
        data: Data to validate
        
    Returns:
        Validated model instance or error response tuple
    """
    try:
        return schema_class(**data)
    except ValidationError as e:
        error_details = []
        for error in e.errors():
            field = " -> ".join(str(x) for x in error['loc'])
            message = error['msg']
            error_details.append(f"{field}: {message}")
        
        return jsonify({
            'error': 'Validation error',
            'details': error_details
        }), 400


def map_db_result_to_schema(db_result: Dict[str, Any], schema_class: BaseModel) -> BaseModel:
    """
    Map database result to Pydantic schema
    
    Args:
        db_result: Database query result
        schema_class: Pydantic model class to map to
        
    Returns:
        Schema instance with mapped data
    """    # Handle JSON fields
    mapped_data = {}
    for key, value in db_result.items():
        if key in ['event_data', 'config'] and value:
            # Parse JSON string to dict if needed
            if isinstance(value, str):
                try:
                    mapped_data[key] = json.loads(value)
                except json.JSONDecodeError:
                    mapped_data[key] = value
            else:
                mapped_data[key] = value
        elif key == 'timestamp' and isinstance(value, str):
            # Handle timestamp strings
            try:
                mapped_data[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                mapped_data[key] = value
        else:
            mapped_data[key] = value
    
    return schema_class(**mapped_data)


def map_db_results_to_schemas(db_results: List[Dict[str, Any]], schema_class: BaseModel) -> List[BaseModel]:
    """
    Map list of database results to Pydantic schemas
    
    Args:
        db_results: List of database query results
        schema_class: Pydantic model class to map to
        
    Returns:
        List of schema instances
    """
    return [map_db_result_to_schema(result, schema_class) for result in db_results]


def create_success_response(schema_class: BaseModel, **kwargs) -> BaseModel:
    """
    Create a success response using a schema
    
    Args:
        schema_class: Response schema class
        **kwargs: Response data
        
    Returns:
        Schema instance with success=True and provided data
    """
    response_data = {'success': True, **kwargs}
    return schema_class(**response_data)


def create_error_response(message: str, details: Optional[Dict[str, Any]] = None, status_code: int = 400) -> tuple:
    """
    Create a standardized error response
    
    Args:
        message: Error message
        details: Optional error details
        status_code: HTTP status code (default: 400)
        
    Returns:
        JSON response tuple with error data and status code
    """
    error_data = {'error': message}
    if details:
        error_data['details'] = details
    
    return jsonify(error_data), status_code


def paginate_results(results: List[Any], page: int, per_page: int) -> Dict[str, Any]:
    """
    Paginate results and return pagination metadata
    
    Args:
        results: List of results to paginate
        page: Current page number
        per_page: Items per page
        
    Returns:
        Dictionary with paginated results and metadata
    """
    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_results = results[start:end]
    has_next = end < total
    
    return {
        'items': paginated_results,
        'page': page,
        'per_page': per_page,
        'total': total,
        'has_next': has_next
    }
