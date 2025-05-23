from flask import Blueprint, request, jsonify
from src.database import db
from src.models.models import Visit, Tag
from datetime import datetime
import uuid

visit_bp = Blueprint('visit', __name__)

@visit_bp.route('/track', methods=['POST'])
def track_visit():
    """Track a website visit"""
    try:
        data = request.get_json()
        
        # Get client information
        page_url = data.get('page_url') or request.referrer
        referrer = data.get('referrer')
        user_agent = request.headers.get('User-Agent')
        ip_address = request.remote_addr
        session_id = data.get('session_id') or str(uuid.uuid4())
        tag_name = data.get('tag')
        
        # Find tag if provided
        tag_id = None
        if tag_name:
            tag = Tag.query.filter_by(name=tag_name, is_active=True).first()
            if tag:
                tag_id = tag.id
        
        # Create new visit record
        visit = Visit(
            page_url=page_url,
            referrer=referrer,
            user_agent=user_agent,
            ip_address=ip_address,
            session_id=session_id,
            tag_id=tag_id,
            timestamp=datetime.utcnow()
        )
        
        db.session.add(visit)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Visit tracked successfully',
            'visit_id': visit.id,
            'session_id': session_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error tracking visit: {str(e)}'
        }), 500

@visit_bp.route('/visits', methods=['GET'])
def get_visits():
    """Get list of visits with optional filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        tag_id = request.args.get('tag_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build query
        query = Visit.query
        
        if tag_id:
            query = query.filter(Visit.tag_id == tag_id)
            
        if start_date:
            start_date = datetime.fromisoformat(start_date)
            query = query.filter(Visit.timestamp >= start_date)
            
        if end_date:
            end_date = datetime.fromisoformat(end_date)
            query = query.filter(Visit.timestamp <= end_date)
        
        # Order by timestamp descending
        query = query.order_by(Visit.timestamp.desc())
        
        # Paginate
        visits = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'visits': [visit.to_dict() for visit in visits.items],
            'pagination': {
                'page': visits.page,
                'pages': visits.pages,
                'per_page': visits.per_page,
                'total': visits.total,
                'has_next': visits.has_next,
                'has_prev': visits.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching visits: {str(e)}'
        }), 500
