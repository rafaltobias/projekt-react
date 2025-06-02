"""
Tracking model using SQLAlchemy ORM instead of raw SQL
"""
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from models.db_models import TrackingEvent
from models.db_instance import db
import logging

logger = logging.getLogger(__name__)

def create_tracking_event(event_data):
    """Create a new tracking event using ORM"""
    try:
        # Create a new TrackingEvent object
        new_event = TrackingEvent(
            session_id=event_data.get('session_id'),
            page_url=event_data.get('page_url'),
            ip_address=event_data.get('ip_address'),
            user_agent=event_data.get('user_agent'),
            referrer=event_data.get('referrer'),
            browser=event_data.get('browser'),
            os=event_data.get('os'),
            device=event_data.get('device'),
            country=event_data.get('country'),
            city=event_data.get('city'),
            is_entry_page=event_data.get('is_entry_page', False),
            is_exit_page=event_data.get('is_exit_page', False),
            event_name=event_data.get('event_name'),
            event_data=event_data.get('event_data'),
            timestamp=datetime.utcnow()
        )
        
        # Add to session and commit
        db.session.add(new_event)
        db.session.commit()
        
        # Return the event ID
        return new_event.id
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error creating tracking event: {str(e)}")
        return None
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating tracking event: {str(e)}")
        return None

def get_tracking_events(page=1, page_size=50, filters=None):
    """Get paginated tracking events with optional filtering"""
    try:
        query = TrackingEvent.query
        
        # Apply filters if provided
        if filters:
            if 'event_name' in filters:
                query = query.filter(TrackingEvent.event_name == filters['event_name'])
            if 'page_url' in filters:
                query = query.filter(TrackingEvent.page_url.like(f"%{filters['page_url']}%"))
            if 'session_id' in filters:
                query = query.filter_by(session_id=filters['session_id'])
            if 'date_from' in filters:
                query = query.filter(TrackingEvent.timestamp >= filters['date_from'])
            if 'date_to' in filters:
                query = query.filter(TrackingEvent.timestamp <= filters['date_to'])
        
        # Get total count for pagination
        total_count = query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        events = query.order_by(TrackingEvent.timestamp.desc()).offset(offset).limit(page_size).all()
        
        # Convert to dictionary
        event_list = [event.to_dict() for event in events]
        
        return {
            'events': event_list,
            'total': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size
        }
    except Exception as e:
        logger.error(f"Error retrieving tracking events: {str(e)}")
        return {
            'events': [],
            'total': 0,
            'page': page,
            'page_size': page_size,
            'total_pages': 0
        }

def get_event_stats(days=30):
    """Get event statistics for a given time period"""
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Query for event counts by name
        event_counts = db.session.query(
            TrackingEvent.event_name, 
            func.count(TrackingEvent.id).label('count')
        ).filter(
            TrackingEvent.timestamp.between(start_date, end_date),
            TrackingEvent.event_name.isnot(None)
        ).group_by(
            TrackingEvent.event_name
        ).order_by(
            desc('count')
        ).all()
        
        # Query for event counts by day
        daily_counts = db.session.query(
            func.date(TrackingEvent.timestamp).label('date'),
            func.count(TrackingEvent.id).label('count')
        ).filter(
            TrackingEvent.timestamp.between(start_date, end_date)
        ).group_by(
            'date'
        ).order_by(
            'date'
        ).all()
        
        # Format results
        event_stats = {
            'by_event': {event.event_name: count for event, count in event_counts},
            'by_day': {str(date): count for date, count in daily_counts}
        }
        
        return event_stats
    except Exception as e:
        logger.error(f"Error retrieving event statistics: {str(e)}")
        return {'by_event': {}, 'by_day': {}}
