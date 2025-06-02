"""
Stats model using SQLAlchemy ORM instead of raw SQL
"""
from sqlalchemy import func, desc, cast, Date
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from models.db_models import Visit, TrackingEvent
from models.db_instance import db
import logging

logger = logging.getLogger(__name__)

def get_visit_stats(days=30):
    """Get visit statistics for the last N days"""
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Query for visits by day
        daily_visits = db.session.query(
            cast(Visit.timestamp, Date).label('date'),
            func.count(Visit.id).label('count')
        ).filter(
            Visit.timestamp.between(start_date, end_date)
        ).group_by(
            'date'
        ).order_by(
            'date'
        ).all()
        
        # Query for top pages
        top_pages = db.session.query(
            Visit.page_url,
            func.count(Visit.id).label('count')
        ).filter(
            Visit.timestamp.between(start_date, end_date)
        ).group_by(
            Visit.page_url
        ).order_by(
            desc('count')
        ).limit(10).all()
        
        # Query for top referrers
        top_referrers = db.session.query(
            Visit.referrer,
            func.count(Visit.id).label('count')
        ).filter(
            Visit.timestamp.between(start_date, end_date),
            Visit.referrer.isnot(None),
            Visit.referrer != ''
        ).group_by(
            Visit.referrer
        ).order_by(
            desc('count')
        ).limit(10).all()
        
        # Query for browser stats
        browsers = db.session.query(
            Visit.browser,
            func.count(Visit.id).label('count')
        ).filter(
            Visit.timestamp.between(start_date, end_date),
            Visit.browser.isnot(None)
        ).group_by(
            Visit.browser
        ).order_by(
            desc('count')
        ).all()
        
        # Query for OS stats
        operating_systems = db.session.query(
            Visit.os,
            func.count(Visit.id).label('count')
        ).filter(
            Visit.timestamp.between(start_date, end_date),
            Visit.os.isnot(None)
        ).group_by(
            Visit.os
        ).order_by(
            desc('count')
        ).all()
        
        # Query for device stats
        devices = db.session.query(
            Visit.device,
            func.count(Visit.id).label('count')
        ).filter(
            Visit.timestamp.between(start_date, end_date),
            Visit.device.isnot(None)
        ).group_by(
            Visit.device
        ).order_by(
            desc('count')
        ).all()
        
        # Query for country stats
        countries = db.session.query(
            Visit.country,
            func.count(Visit.id).label('count')
        ).filter(
            Visit.timestamp.between(start_date, end_date),
            Visit.country.isnot(None),
            Visit.country != ''
        ).group_by(
            Visit.country
        ).order_by(
            desc('count')
        ).all()
        
        # Format results
        stats = {
            'total_visits': sum(count for _, count in daily_visits),
            'daily_visits': {str(date): count for date, count in daily_visits},
            'top_pages': {url: count for url, count in top_pages},
            'top_referrers': {ref if ref else 'Direct': count for ref, count in top_referrers},
            'browsers': {browser if browser else 'Unknown': count for browser, count in browsers},
            'operating_systems': {os if os else 'Unknown': count for os, count in operating_systems},
            'devices': {device if device else 'Unknown': count for device, count in devices},
            'countries': {country if country else 'Unknown': count for country, count in countries}
        }
        
        return stats
    except Exception as e:
        logger.error(f"Error retrieving visit statistics: {str(e)}")
        return {
            'total_visits': 0,
            'daily_visits': {},
            'top_pages': {},
            'top_referrers': {},
            'browsers': {},
            'operating_systems': {},
            'devices': {},
            'countries': {}
        }

def get_tracking_stats(days=30):
    """Get tracking event statistics"""
    try:
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Query for events by name
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
        
        # Format results
        stats = {
            'total_events': sum(count for _, count in event_counts),
            'events_by_type': {event_name: count for event_name, count in event_counts}
        }
        
        return stats
    except Exception as e:
        logger.error(f"Error retrieving tracking statistics: {str(e)}")
        return {
            'total_events': 0,
            'events_by_type': {}
        }

def get_export_data(start_date=None, end_date=None, include_events=True):
    """Get all visit and event data for export"""
    try:
        # Prepare date filters
        filters = []
        if start_date:
            filters.append(Visit.timestamp >= start_date)
        if end_date:
            filters.append(Visit.timestamp <= end_date)
            
        # Get all visits
        visits_query = Visit.query.filter(*filters).order_by(Visit.timestamp.desc())
        visits = [visit.to_dict() for visit in visits_query.all()]
        
        # Get event data if requested
        events = []
        if include_events:
            event_filters = []
            if start_date:
                event_filters.append(TrackingEvent.timestamp >= start_date)
            if end_date:
                event_filters.append(TrackingEvent.timestamp <= end_date)
                
            events_query = TrackingEvent.query.filter(*event_filters).order_by(TrackingEvent.timestamp.desc())
            events = [event.to_dict() for event in events_query.all()]
        
        return {
            'visits': visits,
            'events': events
        }
    except Exception as e:
        logger.error(f"Error retrieving export data: {str(e)}")
        return {
            'visits': [],
            'events': []
        }
