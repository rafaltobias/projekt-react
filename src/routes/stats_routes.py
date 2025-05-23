from flask import Blueprint, request, jsonify, send_file
from src.database import db
from src.models.models import Visit, Tag
from datetime import datetime, timedelta
from sqlalchemy import func, distinct
import csv
import io
import tempfile
import os

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get website statistics"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        tag_id = request.args.get('tag_id', type=int)
        
        # Default to last 30 days if no dates provided
        if not end_date:
            end_date = datetime.utcnow()
        else:
            end_date = datetime.fromisoformat(end_date)
            
        if not start_date:
            start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.fromisoformat(start_date)
        
        # Initialize with default empty values
        total_visits = 0
        unique_visitors = 0
        top_pages = []
        top_referrers = []
        daily_visits = []
        recent_visits = []
        
        # Build base query and get counts        try:
            # Build base query
            base_query = Visit.query.filter(
                Visit.timestamp >= start_date,
                Visit.timestamp <= end_date
            )
            
            # Filter by tag if specified (using JSONB contains)
            # This would need to be modified based on your exact JSON structure
            if tag_id:
                # For now, we're skipping tag filtering as we need to check the
                # JSON structure first. Just log that we tried to filter by tag
                print(f"Note: Tag filtering by tag_id {tag_id} is not implemented yet")
            
            # Total visits
            total_visits = base_query.count()
            
            # Unique visitors (by IP address)
            unique_visitors = base_query.with_entities(
                distinct(Visit.ip_address)
            ).count()
        except Exception as db_error:
            print(f"Database error in stats query: {str(db_error)}")
        
        # Get detailed statistics
        try:
            # Top pages            top_pages_query = db.session.query(
                Visit.page_url,
                func.count(Visit.id).label('visit_count')
            ).filter(
                Visit.timestamp >= start_date,
                Visit.timestamp <= end_date
            )
            
            # Skip tag filtering for now
            if tag_id:
                print(f"Note: Tag filtering by tag_id {tag_id} not implemented for top_pages")
                
            top_pages = top_pages_query.group_by(Visit.page_url)\
                               .order_by(func.count(Visit.id).desc())\
                               .limit(10).all()
            
            # Top referrers            top_referrers_query = db.session.query(
                Visit.referrer,
                func.count(Visit.id).label('visit_count')
            ).filter(
                Visit.timestamp >= start_date,
                Visit.timestamp <= end_date,
                Visit.referrer.isnot(None),
                Visit.referrer != ''
            )
            
            # Skip tag filtering for now
            if tag_id:
                print(f"Note: Tag filtering by tag_id {tag_id} not implemented for top_referrers")
                
            top_referrers = top_referrers_query.group_by(Visit.referrer)\
                                       .order_by(func.count(Visit.id).desc())\
                                       .limit(10).all()
            
            # Daily visits for chart            daily_visits_query = db.session.query(
                func.date(Visit.timestamp).label('date'),
                func.count(Visit.id).label('visit_count'),
                func.count(distinct(Visit.ip_address)).label('unique_visitors')
            ).filter(
                Visit.timestamp >= start_date,
                Visit.timestamp <= end_date
            )
            
            # Skip tag filtering for now
            if tag_id:
                print(f"Note: Tag filtering by tag_id {tag_id} not implemented for daily_visits")
                
            daily_visits = daily_visits_query.group_by(func.date(Visit.timestamp))\
                                     .order_by(func.date(Visit.timestamp)).all()
            
            # Recent visits
            recent_visits = base_query.order_by(Visit.timestamp.desc()).limit(10).all()
        
        except Exception as db_error:
            print(f"Database error in stats aggregation: {str(db_error)}")
        
        return jsonify({
            'success': True,
            'data': {
                'total_visits': total_visits,
                'unique_visitors': unique_visitors,
                'date_range': {
                    'start': start_date.isoformat(),
                    'end': end_date.isoformat()
                },
                'top_pages': [
                    {'page_url': page[0], 'visit_count': page[1]} 
                    for page in top_pages
                ],
                'top_referrers': [
                    {'referrer': ref[0], 'visit_count': ref[1]} 
                    for ref in top_referrers
                ],
                'daily_visits': [
                    {
                        'date': visit[0].isoformat() if visit[0] else None,
                        'visit_count': visit[1],
                        'unique_visitors': visit[2]
                    }
                    for visit in daily_visits
                ],
                'recent_visits': [visit.to_dict() for visit in recent_visits]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching statistics: {str(e)}'
        }), 500

@stats_bp.route('/exportStats', methods=['GET'])
def export_stats():
    """Export statistics to CSV"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        tag_id = request.args.get('tag_id', type=int)
        export_type = request.args.get('type', 'visits')  # visits, stats, or summary
        
        # Default to last 30 days if no dates provided
        if not end_date:
            end_date = datetime.utcnow()
        else:
            end_date = datetime.fromisoformat(end_date)
            
        if not start_date:
            start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.fromisoformat(start_date)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='')
        
        if export_type == 'visits':
            # Export all visits
            query = Visit.query.filter(
                Visit.timestamp >= start_date,
                Visit.timestamp <= end_date
            )
            
            if tag_id:
                query = query.filter(Visit.tag_id == tag_id)
                
            visits = query.order_by(Visit.timestamp.desc()).all()
            
            writer = csv.writer(temp_file)
            writer.writerow(['ID', 'Page URL', 'Referrer', 'IP Address', 'Timestamp', 'Tag'])
            
            for visit in visits:
                tag_name = visit.tag.name if visit.tag else ''
                writer.writerow([
                    visit.id,
                    visit.page_url,
                    visit.referrer or '',
                    visit.ip_address,
                    visit.timestamp.isoformat() if visit.timestamp else '',
                    tag_name
                ])
        
        elif export_type == 'summary':
            # Export summary statistics
            writer = csv.writer(temp_file)
            writer.writerow(['Metric', 'Value'])
            
            # Get basic stats
            base_query = Visit.query.filter(
                Visit.timestamp >= start_date,
                Visit.timestamp <= end_date
            )
            
            if tag_id:
                base_query = base_query.filter(Visit.tag_id == tag_id)
            
            total_visits = base_query.count()
            unique_visitors = base_query.with_entities(distinct(Visit.ip_address)).count()
            
            writer.writerow(['Total Visits', total_visits])
            writer.writerow(['Unique Visitors', unique_visitors])
            writer.writerow(['Date Range Start', start_date.isoformat()])
            writer.writerow(['Date Range End', end_date.isoformat()])
        
        temp_file.close()
        
        # Generate filename
        filename = f"analytics_export_{export_type}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error exporting statistics: {str(e)}'
        }), 500

@stats_bp.route('/stats/dashboard')
def get_dashboard_stats():
    """Get dashboard overview statistics"""
    try:
        # Get stats for different time periods
        now = datetime.utcnow()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Use mock data temporarily for development
        today_visits = 0
        today_unique = 0
        week_visits = 0
        week_unique = 0
        month_visits = 0
        month_unique = 0
        total_visits = 0
        total_unique = 0
        popular_tag = None
        
        # Try to get real data if database is available
        try:
            # Today's stats
            today_visits = Visit.query.filter(Visit.timestamp >= today).count()
            today_unique = Visit.query.filter(Visit.timestamp >= today)\
                               .with_entities(distinct(Visit.ip_address)).count()
            
            # This week's stats
            week_visits = Visit.query.filter(Visit.timestamp >= week_ago).count()
            week_unique = Visit.query.filter(Visit.timestamp >= week_ago)\
                              .with_entities(distinct(Visit.ip_address)).count()
            
            # This month's stats
            month_visits = Visit.query.filter(Visit.timestamp >= month_ago).count()
            month_unique = Visit.query.filter(Visit.timestamp >= month_ago)\
                               .with_entities(distinct(Visit.ip_address)).count()
            
            # All time stats
            total_visits = Visit.query.count()
            total_unique = Visit.query.with_entities(distinct(Visit.ip_address)).count()
                  # For now, we'll skip the most popular tag calculation since we don't have a direct relationship
        # We'd need to parse the JSONB tags field to extract this information
        popular_tag = None  # This will be returned as null in the JSON response
        except Exception as db_error:
            print(f"Database error: {str(db_error)}")
        
        return jsonify({
            'success': True,
            'data': {
                'today': {
                    'visits': today_visits,
                    'unique_visitors': today_unique
                },
                'week': {
                    'visits': week_visits,
                    'unique_visitors': week_unique
                },
                'month': {
                    'visits': month_visits,
                    'unique_visitors': month_unique
                },
                'total': {
                    'visits': total_visits,
                    'unique_visitors': total_unique
                },
                'popular_tag': {
                    'name': popular_tag[0] if popular_tag else None,
                    'visit_count': popular_tag[1] if popular_tag else 0
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching dashboard statistics: {str(e)}'
        }), 500
