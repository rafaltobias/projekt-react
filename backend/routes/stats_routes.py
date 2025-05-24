from flask import Blueprint, request, jsonify, render_template, send_file
from models.stats_model import get_visit_stats, generate_stats_csv
from datetime import datetime
import io

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        stats = get_visit_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@stats_bp.route('/stats', methods=['GET'])
def get_stats_page():
    # This route will be handled by the React frontend
    return render_template('index.html')

@stats_bp.route('/api/exportStats', methods=['GET'])
def export_stats():
    try:
        csv_buffer = generate_stats_csv()
        if not csv_buffer:
            return jsonify({'error': 'No data available'}), 404
            
        # Generate filename with current date
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"visit-stats-{date_str}.csv"
        
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
        return jsonify({'error': str(e)}), 500
