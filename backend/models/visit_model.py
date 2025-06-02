"""
Visit model using SQLAlchemy ORM instead of raw SQL
"""
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models.db_models import Visit
from models.db_instance import db
import logging

logger = logging.getLogger(__name__)

def create_visit(visit_data):
    """Create a new visit record using ORM"""
    try:
        # Create a new Visit object
        new_visit = Visit(
            page_url=visit_data.get('page_url'),
            ip_address=visit_data.get('ip_address'),
            user_agent=visit_data.get('user_agent'),
            referrer=visit_data.get('referrer'),
            browser=visit_data.get('browser'),
            os=visit_data.get('os'),
            device=visit_data.get('device'),
            country=visit_data.get('country'),
            session_id=visit_data.get('session_id'),
            is_entry_page=visit_data.get('is_entry_page', False),
            is_exit_page=visit_data.get('is_exit_page', False),
            event_name=visit_data.get('event_name'),
            event_data=visit_data.get('event_data'),
            timestamp=datetime.utcnow()
        )
        
        # Add to session and commit
        db.session.add(new_visit)
        db.session.commit()
        
        # Return the visit ID
        return new_visit.id
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error creating visit: {str(e)}")
        return None
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating visit: {str(e)}")
        return None

def get_visit_by_id(visit_id):
    """Get a visit by ID"""
    try:
        visit = Visit.query.filter_by(id=visit_id).first()
        return visit.to_dict() if visit else None
    except Exception as e:
        logger.error(f"Error retrieving visit by ID: {str(e)}")
        return None

def get_visits_paginated(page=1, page_size=50, filters=None):
    """Get paginated visits with optional filtering"""
    try:
        query = Visit.query
        
        # Apply filters if provided
        if filters:
            if 'page_url' in filters:
                query = query.filter(Visit.page_url.like(f"%{filters['page_url']}%"))
            if 'session_id' in filters:
                query = query.filter_by(session_id=filters['session_id'])
            if 'date_from' in filters:
                query = query.filter(Visit.timestamp >= filters['date_from'])
            if 'date_to' in filters:
                query = query.filter(Visit.timestamp <= filters['date_to'])
            if 'country' in filters:
                query = query.filter_by(country=filters['country'])
        
        # Get total count for pagination
        total_count = query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        visits = query.order_by(Visit.timestamp.desc()).offset(offset).limit(page_size).all()
        
        # Convert to dictionary
        visit_list = [visit.to_dict() for visit in visits]
        
        return {
            'visits': visit_list,
            'total': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size
        }
    except Exception as e:
        logger.error(f"Error retrieving paginated visits: {str(e)}")
        return {
            'visits': [],
            'total': 0,
            'page': page,
            'page_size': page_size,
            'total_pages': 0
        }

def update_visit(visit_id, visit_data):
    """Update an existing visit"""
    try:
        visit = Visit.query.get(visit_id)
        if not visit:
            return False
        
        # Update fields
        for key, value in visit_data.items():
            if hasattr(visit, key):
                setattr(visit, key, value)
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating visit: {str(e)}")
        return False

def delete_visit(visit_id):
    """Delete a visit by ID"""
    try:
        visit = Visit.query.get(visit_id)
        if not visit:
            return False
        
        db.session.delete(visit)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting visit: {str(e)}")
        return False
