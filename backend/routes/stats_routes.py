from flask import Blueprint, request, jsonify, render_template, send_file
from flask_restx import Namespace, Resource
from services.stats_service import StatsService
from services.file_serving_service import FileServingService
from schemas.stats_schemas import VisitStatsResponse, ComprehensiveStatsResponse
from schemas.base_schemas import ErrorResponse
from utils.validation import create_error_response
from datetime import datetime
import io
import logging

logger = logging.getLogger(__name__)

stats_bp = Blueprint('stats', __name__)

# Create API namespace for this blueprint  
api = Namespace('stats', description='Statistics endpoints')


@stats_bp.route('/api/stats', methods=['GET'])
@api.response(200, 'Statistics retrieved successfully')
@api.response(500, 'Internal server error')
def get_stats():
    """Get visit statistics"""
    try:
        stats_data = StatsService.get_visit_stats()
        
        # Create response using schema
        response = VisitStatsResponse(
            total_visits=stats_data.get('total_visits', 0),
            unique_visitors=stats_data.get('unique_visitors', 0),
            page_views=stats_data.get('page_views', 0),
            bounce_rate=stats_data.get('bounce_rate', 0.0),
            average_session_duration=stats_data.get('average_session_duration'),
            top_pages=stats_data.get('top_pages', []),
            top_referrers=stats_data.get('top_referrers', []),
            countries=stats_data.get('countries', []),
            browsers=stats_data.get('browsers', []),
            operating_systems=stats_data.get('operating_systems', []),
            devices=stats_data.get('devices', []),
            hourly_visits=stats_data.get('hourly_visits', []),
            daily_visits=stats_data.get('daily_visits', [])
        )
        
        return jsonify(response.model_dump())
        
    except Exception as e:
        logger.error(f"Failed to retrieve statistics: {str(e)}")
        return create_error_response(f'Failed to retrieve statistics: {str(e)}', status_code=500)

@stats_bp.route('/stats', methods=['GET'])
def get_stats_page():
    # This route will be handled by the React frontend
    return render_template('index.html')

@stats_bp.route('/api/exportStats', methods=['GET'])
def export_stats():
    """Export visit statistics as CSV"""
    try:
        # Prepare CSV using service business logic
        csv_buffer = StatsService.prepare_csv_export()
        if not csv_buffer:
            return jsonify({'error': 'No data available'}), 404
            
        # Generate filename using service
        filename = StatsService.generate_export_filename('csv')
        
        # Convert StringIO to BytesIO for send_file
        bytes_io = io.BytesIO(csv_buffer.getvalue().encode('utf-8'))
        bytes_io.seek(0)
        
        return send_file(
            bytes_io,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"Failed to export statistics: {str(e)}")
        return jsonify({'error': str(e)}), 500
