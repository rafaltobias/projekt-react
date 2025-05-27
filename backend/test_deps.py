#!/usr/bin/env python3
import sys
sys.path.append('.')

# Test imports one by one
try:
    from flask import Blueprint, request, jsonify
    print("✓ Flask imports OK")
except Exception as e:
    print(f"✗ Flask imports failed: {e}")

try:
    from flask_restx import Api, Resource, fields
    print("✓ Flask-RESTX imports OK")
except Exception as e:
    print(f"✗ Flask-RESTX imports failed: {e}")

try:
    from pydantic import ValidationError
    print("✓ Pydantic imports OK")
except Exception as e:
    print(f"✗ Pydantic imports failed: {e}")

try:
    from models.tag_model import create_tag, get_all_tags, get_tag_by_id, delete_tag
    print("✓ Tag model imports OK")
except Exception as e:
    print(f"✗ Tag model imports failed: {e}")

try:
    from schemas.tag_schemas import TagRequest, TagResponse, TagCreateResponse, TagsListResponse
    print("✓ Tag schemas imports OK")
except Exception as e:
    print(f"✗ Tag schemas imports failed: {e}")

try:
    from schemas.base_schemas import BaseResponse, ErrorResponse
    print("✓ Base schemas imports OK")
except Exception as e:
    print(f"✗ Base schemas imports failed: {e}")

try:
    from utils.validation import (
        validate_request_data, map_db_result_to_schema, map_db_results_to_schemas,
        create_success_response, create_error_response
    )
    print("✓ Validation utils imports OK")
except Exception as e:
    print(f"✗ Validation utils imports failed: {e}")
