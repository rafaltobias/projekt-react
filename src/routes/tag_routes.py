from flask import Blueprint, request, jsonify
from src.database import db
from src.models.models import Tag, Visit
from sqlalchemy import func
from datetime import datetime

tag_bp = Blueprint('tag', __name__)

@tag_bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all tags with visit counts"""
    try:
        # Get query parameters
        include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
        
        query = Tag.query
        if not include_inactive:
            query = query.filter(Tag.is_active == True)
          # Get all tags without calculating visit count since we don't have a direct relation
        tags = query.order_by(Tag.name).all()
        
        # We'll set visit_count to 0 for now
        tags_with_counts = [(tag, 0) for tag in tags]
        
        tags_data = []
        for tag, visit_count in tags_with_counts:
            tag_dict = tag.to_dict()
            tag_dict['visit_count'] = visit_count
            tags_data.append(tag_dict)
        
        return jsonify({
            'success': True,
            'tags': tags_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching tags: {str(e)}'
        }), 500

@tag_bp.route('/tags/<int:tag_id>', methods=['GET'])
def get_tag_by_id(tag_id):
    """Get a specific tag by ID"""
    try:
        tag = Tag.query.get_or_404(tag_id)
          # Since we don't have a direct relation, setting visit count to 0
        visit_count = 0
        
        tag_data = tag.to_dict()
        tag_data['visit_count'] = visit_count
        
        return jsonify({
            'success': True,
            'tag': tag_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching tag: {str(e)}'
        }), 500

@tag_bp.route('/tags', methods=['POST'])
def create_tag():
    """Create a new tag"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('name'):
            return jsonify({
                'success': False,
                'message': 'Tag name is required'
            }), 400
        
        # Check if tag name already exists
        existing_tag = Tag.query.filter_by(name=data['name']).first()
        if existing_tag:
            return jsonify({
                'success': False,
                'message': 'Tag with this name already exists'
            }), 409
        
        # Create new tag
        tag = Tag(
            name=data['name'],
            description=data.get('description', ''),
            color=data.get('color', '#3B82F6'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(tag)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tag created successfully',
            'tag': tag.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating tag: {str(e)}'
        }), 500

@tag_bp.route('/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    """Update an existing tag"""
    try:
        tag = Tag.query.get_or_404(tag_id)
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Check if new name conflicts with existing tags (excluding current tag)
        if 'name' in data and data['name'] != tag.name:
            existing_tag = Tag.query.filter_by(name=data['name']).first()
            if existing_tag:
                return jsonify({
                    'success': False,
                    'message': 'Tag with this name already exists'
                }), 409
        
        # Update tag fields
        if 'name' in data:
            tag.name = data['name']
        if 'description' in data:
            tag.description = data['description']
        if 'color' in data:
            tag.color = data['color']
        if 'is_active' in data:
            tag.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tag updated successfully',
            'tag': tag.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating tag: {str(e)}'
        }), 500

@tag_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    """Delete a tag (soft delete by setting is_active to False)"""
    try:
        tag = Tag.query.get_or_404(tag_id)
          # Since we don't have a direct relation, setting visit count to 0
        visit_count = 0
        
        force_delete = request.args.get('force', 'false').lower() == 'true'
        
        if visit_count > 0 and not force_delete:
            # Soft delete - just mark as inactive
            tag.is_active = False
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Tag deactivated (has {visit_count} associated visits). Use force=true to permanently delete.',
                'soft_delete': True
            }), 200
        else:
            # Hard delete - remove completely
            db.session.delete(tag)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Tag deleted successfully',
                'soft_delete': False
            }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting tag: {str(e)}'
        }), 500

@tag_bp.route('/tags/<int:tag_id>/stats', methods=['GET'])
def get_tag_stats(tag_id):
    """Get statistics for a specific tag"""
    try:
        tag = Tag.query.get_or_404(tag_id)
        
        # Get date range parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Default to last 30 days if no dates provided
        if not end_date:
            end_date = datetime.utcnow()
        else:
            end_date = datetime.fromisoformat(end_date)
            
        if not start_date:
            start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.fromisoformat(start_date)
        
        # Get visits for this tag in date range
        visits_query = Visit.query.filter(
            Visit.tag_id == tag_id,
            Visit.timestamp >= start_date,
            Visit.timestamp <= end_date
        )
        
        total_visits = visits_query.count()
        unique_visitors = visits_query.with_entities(func.count(func.distinct(Visit.ip_address))).scalar()
        
        # Daily breakdown
        daily_stats = db.session.query(
            func.date(Visit.timestamp).label('date'),
            func.count(Visit.id).label('visit_count'),
            func.count(func.distinct(Visit.ip_address)).label('unique_visitors')
        ).filter(
            Visit.tag_id == tag_id,
            Visit.timestamp >= start_date,
            Visit.timestamp <= end_date
        ).group_by(func.date(Visit.timestamp))\
         .order_by(func.date(Visit.timestamp)).all()
        
        # Top pages for this tag
        top_pages = db.session.query(
            Visit.page_url,
            func.count(Visit.id).label('visit_count')
        ).filter(
            Visit.tag_id == tag_id,
            Visit.timestamp >= start_date,
            Visit.timestamp <= end_date
        ).group_by(Visit.page_url)\
         .order_by(func.count(Visit.id).desc())\
         .limit(10).all()
        
        return jsonify({
            'success': True,
            'tag': tag.to_dict(),
            'stats': {
                'total_visits': total_visits,
                'unique_visitors': unique_visitors,
                'date_range': {
                    'start': start_date.isoformat(),
                    'end': end_date.isoformat()
                },
                'daily_stats': [
                    {
                        'date': stat[0].isoformat() if stat[0] else None,
                        'visit_count': stat[1],
                        'unique_visitors': stat[2]
                    }
                    for stat in daily_stats
                ],
                'top_pages': [
                    {'page_url': page[0], 'visit_count': page[1]}
                    for page in top_pages
                ]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching tag statistics: {str(e)}'
        }), 500
