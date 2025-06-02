"""
Statistics service - business logic for comprehensive analytics
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import func, desc, and_
from models.db_instance import db
from models.db_models import Visit
from services.base_service import BaseService
import logging
import csv
import io

logger = logging.getLogger(__name__)


class StatsService(BaseService):
    """Service for statistics and analytics operations"""
    
    @staticmethod
    def get_visit_stats() -> Dict[str, Any]:
        """Get comprehensive visit statistics"""
        try:
            # Total visits
            total_visits = Visit.query.count()
            
            # Unique visitors (by IP)
            unique_visitors = db.session.query(func.count(func.distinct(Visit.ip_address))).scalar()
            
            # Page views (visits without event_name or with event_name='page_view')
            page_views = Visit.query.filter(
                (Visit.event_name.is_(None)) | (Visit.event_name == 'page_view')
            ).count()
            
            # Calculate bounce rate (sessions with only one page view)
            session_counts = db.session.query(
                Visit.session_id,
                func.count(Visit.id).label('page_count')
            ).filter(
                Visit.session_id.isnot(None),
                (Visit.event_name.is_(None)) | (Visit.event_name == 'page_view')
            ).group_by(Visit.session_id).subquery()
            
            total_sessions = db.session.query(func.count()).select_from(session_counts).scalar()
            bounce_sessions = db.session.query(func.count()).select_from(session_counts).filter(
                session_counts.c.page_count == 1
            ).scalar()
            
            bounce_rate = (bounce_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            # Average session duration
            session_durations = db.session.query(
                Visit.session_id,
                (func.max(Visit.timestamp) - func.min(Visit.timestamp)).label('duration')
            ).filter(
                Visit.session_id.isnot(None)
            ).group_by(Visit.session_id).having(
                func.count(Visit.id) > 1
            ).all()
            
            if session_durations:
                avg_duration = sum(d.duration.total_seconds() for d in session_durations) / len(session_durations)
                avg_duration = avg_duration / 60  # Convert to minutes
            else:
                avg_duration = None
            
            # Top pages
            top_pages = db.session.query(
                Visit.page_url,
                func.count(Visit.id).label('count')
            ).group_by(Visit.page_url).order_by(desc('count')).limit(10).all()
            
            # Top referrers
            top_referrers = db.session.query(
                Visit.referrer,
                func.count(Visit.id).label('count')
            ).filter(
                Visit.referrer.isnot(None),
                Visit.referrer != ''
            ).group_by(Visit.referrer).order_by(desc('count')).limit(10).all()
            
            # Countries
            countries = db.session.query(
                Visit.country,
                func.count(Visit.id).label('count')
            ).filter(
                Visit.country.isnot(None)
            ).group_by(Visit.country).order_by(desc('count')).limit(10).all()
            
            # Browsers
            browsers = db.session.query(
                Visit.browser,
                func.count(Visit.id).label('count')
            ).filter(
                Visit.browser.isnot(None)
            ).group_by(Visit.browser).order_by(desc('count')).limit(10).all()
            
            # Operating systems
            operating_systems = db.session.query(
                Visit.os,
                func.count(Visit.id).label('count')
            ).filter(
                Visit.os.isnot(None)
            ).group_by(Visit.os).order_by(desc('count')).limit(10).all()
            
            # Devices
            devices = db.session.query(
                Visit.device,
                func.count(Visit.id).label('count')
            ).filter(
                Visit.device.isnot(None)
            ).group_by(Visit.device).order_by(desc('count')).limit(10).all()
            
            # Hourly visits (last 24 hours)
            last_24h = datetime.utcnow() - timedelta(hours=24)
            hourly_visits = db.session.query(
                func.extract('hour', Visit.timestamp).label('hour'),
                func.count(Visit.id).label('count')
            ).filter(
                Visit.timestamp >= last_24h
            ).group_by(func.extract('hour', Visit.timestamp)).order_by('hour').all()
            
            # Daily visits (last 30 days)
            last_30d = datetime.utcnow() - timedelta(days=30)
            daily_visits = db.session.query(
                func.date(Visit.timestamp).label('date'),
                func.count(Visit.id).label('count')
            ).filter(
                Visit.timestamp >= last_30d
            ).group_by(func.date(Visit.timestamp)).order_by('date').all()
            
            return {
                'total_visits': total_visits,
                'unique_visitors': unique_visitors,
                'page_views': page_views,
                'bounce_rate': round(bounce_rate, 2),
                'average_session_duration': round(avg_duration, 2) if avg_duration else None,
                'top_pages': [{'page_url': p.page_url, 'count': p.count} for p in top_pages],
                'top_referrers': [{'referrer': r.referrer, 'count': r.count} for r in top_referrers],
                'countries': [{'country': c.country, 'count': c.count} for c in countries],
                'browsers': [{'browser': b.browser, 'count': b.count} for b in browsers],
                'operating_systems': [{'os': o.os, 'count': o.count} for o in operating_systems],
                'devices': [{'device': d.device, 'count': d.count} for d in devices],
                'hourly_visits': [{'hour': int(h.hour), 'count': h.count} for h in hourly_visits],
                'daily_visits': [{'date': d.date.strftime('%Y-%m-%d'), 'count': d.count} for d in daily_visits]
            }
            
        except Exception as e:
            logger.error(f"Error getting visit statistics: {str(e)}")
            # Return default structure to prevent frontend errors
            return {
                'total_visits': 0,
                'unique_visitors': 0,
                'page_views': 0,
                'bounce_rate': 0.0,
                'average_session_duration': None,
                'top_pages': [],
                'top_referrers': [],
                'countries': [],
                'browsers': [],
                'operating_systems': [],
                'devices': [],
                'hourly_visits': [],
                'daily_visits': []
            }
    
    @staticmethod
    def generate_stats_csv() -> Optional[io.StringIO]:
        """Generate CSV file with visit statistics"""
        try:
            visits = Visit.query.order_by(desc(Visit.timestamp)).all()
            
            if not visits:
                return None
            
            # Create in-memory CSV file
            output = io.StringIO()
            fieldnames = [
                'id', 'timestamp', 'page_url', 'referrer', 'user_agent', 'ip_address',
                'browser', 'os', 'device', 'country', 'session_id', 
                'is_entry_page', 'is_exit_page', 'event_name', 'event_data'
            ]
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            
            writer.writeheader()
            for visit in visits:
                writer.writerow({
                    'id': visit.id,
                    'timestamp': visit.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'page_url': visit.page_url,
                    'referrer': visit.referrer,
                    'user_agent': visit.user_agent,
                    'ip_address': visit.ip_address,
                    'browser': visit.browser,
                    'os': visit.os,
                    'device': visit.device,
                    'country': visit.country,
                    'session_id': visit.session_id,
                    'is_entry_page': visit.is_entry_page,
                    'is_exit_page': visit.is_exit_page,
                    'event_name': visit.event_name,
                    'event_data': str(visit.event_data) if visit.event_data else None
                })
            
            output.seek(0)
            logger.info(f"Generated CSV with {len(visits)} visits")
            return output
            
        except Exception as e:
            logger.error(f"Error generating stats CSV: {str(e)}")
            return None
    
    @staticmethod
    def get_comprehensive_stats(days: int = 30) -> Dict[str, Any]:
        """Get comprehensive statistics for a specified time period"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Total page views
            total_page_views = Visit.query.filter(
                Visit.timestamp >= cutoff_date,
                (Visit.event_name.is_(None)) | (Visit.event_name == 'page_view')
            ).count()
            
            # Unique sessions
            unique_sessions = db.session.query(
                func.count(func.distinct(Visit.session_id))
            ).filter(
                Visit.timestamp >= cutoff_date,
                Visit.session_id.isnot(None)
            ).scalar()
            
            # Average session duration
            session_durations = db.session.query(
                Visit.session_id,
                (func.max(Visit.timestamp) - func.min(Visit.timestamp)).label('duration')
            ).filter(
                Visit.timestamp >= cutoff_date,
                Visit.session_id.isnot(None)
            ).group_by(Visit.session_id).having(
                func.count(Visit.id) > 1
            ).all()
            
            avg_session_duration = 0
            if session_durations:
                avg_duration = sum(d.duration.total_seconds() for d in session_durations) / len(session_durations)
                avg_session_duration = round(avg_duration / 60, 2)  # Convert to minutes
            
            # Daily stats
            daily_stats = db.session.query(
                func.date(Visit.timestamp).label('date'),
                func.count(Visit.id).label('page_views')
            ).filter(
                Visit.timestamp >= cutoff_date,
                (Visit.event_name.is_(None)) | (Visit.event_name == 'page_view')
            ).group_by(func.date(Visit.timestamp)).order_by(desc('date')).all()
            
            # Top pages
            top_pages = db.session.query(
                Visit.page_url,
                func.count(Visit.id).label('views')
            ).filter(
                Visit.timestamp >= cutoff_date,
                (Visit.event_name.is_(None)) | (Visit.event_name == 'page_view')
            ).group_by(Visit.page_url).order_by(desc('views')).limit(10).all()
            
            # Top referrers
            top_referrers = db.session.query(
                Visit.referrer,
                func.count(Visit.id).label('count')
            ).filter(
                Visit.timestamp >= cutoff_date,
                Visit.referrer.isnot(None),
                Visit.referrer != ''
            ).group_by(Visit.referrer).order_by(desc('count')).limit(10).all()
            
            # Browser stats
            browser_stats = db.session.query(
                Visit.browser,
                func.count(Visit.id).label('count')
            ).filter(
                Visit.timestamp >= cutoff_date,
                Visit.browser.isnot(None)
            ).group_by(Visit.browser).order_by(desc('count')).limit(10).all()
            
            # OS stats
            os_stats = db.session.query(
                Visit.os,
                func.count(Visit.id).label('count')
            ).filter(
                Visit.timestamp >= cutoff_date,
                Visit.os.isnot(None)
            ).group_by(Visit.os).order_by(desc('count')).limit(10).all()
            
            # Device stats
            device_stats = db.session.query(
                Visit.device,
                func.count(Visit.id).label('count')
            ).filter(
                Visit.timestamp >= cutoff_date,
                Visit.device.isnot(None)
            ).group_by(Visit.device).order_by(desc('count')).limit(5).all()
            
            # Country stats
            country_stats = db.session.query(
                Visit.country,
                func.count(Visit.id).label('count')
            ).filter(
                Visit.timestamp >= cutoff_date,
                Visit.country.isnot(None)
            ).group_by(Visit.country).order_by(desc('count')).limit(10).all()
            
            return {
                'total_page_views': total_page_views,
                'unique_sessions': unique_sessions,
                'avg_session_duration': avg_session_duration,
                'daily_stats': [{'date': d.date.strftime('%Y-%m-%d'), 'page_views': d.page_views} for d in daily_stats],
                'top_pages': [{'page_url': p.page_url, 'views': p.views} for p in top_pages],
                'top_referrers': [{'referrer': r.referrer, 'count': r.count} for r in top_referrers],
                'browser_stats': [{'browser': b.browser, 'count': b.count} for b in browser_stats],
                'os_stats': [{'os': o.os, 'count': o.count} for o in os_stats],
                'device_stats': [{'device': d.device, 'count': d.count} for d in device_stats],
                'country_stats': [{'country': c.country, 'count': c.count} for c in country_stats]
            }
            
        except Exception as e:
            logger.error(f"Error getting comprehensive stats: {str(e)}")
            return {
                'total_page_views': 0,
                'unique_sessions': 0,
                'avg_session_duration': 0,
                'daily_stats': [],
                'top_pages': [],
                'top_referrers': [],
                'browser_stats': [],
                'os_stats': [],
                'device_stats': [],
                'country_stats': []
            }
    
    @staticmethod
    def get_realtime_stats() -> Dict[str, Any]:
        """Get real-time statistics"""
        try:
            now = datetime.utcnow()
            
            # Active sessions (last 30 minutes)
            active_sessions = db.session.query(
                func.count(func.distinct(Visit.session_id))
            ).filter(
                Visit.timestamp >= now - timedelta(minutes=30),
                Visit.session_id.isnot(None)
            ).scalar()
            
            # Page views in last hour
            hourly_views = Visit.query.filter(
                Visit.timestamp >= now - timedelta(hours=1),
                (Visit.event_name.is_(None)) | (Visit.event_name == 'page_view')
            ).count()
            
            # Most visited page today
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            top_pages_today = db.session.query(
                Visit.page_url,
                func.count(Visit.id).label('views')
            ).filter(
                Visit.timestamp >= today_start,
                (Visit.event_name.is_(None)) | (Visit.event_name == 'page_view')
            ).group_by(Visit.page_url).order_by(desc('views')).limit(5).all()
            
            # Recent visits (last 10)
            recent_visits = Visit.query.order_by(desc(Visit.timestamp)).limit(10).all()
            
            return {
                'active_sessions': active_sessions,
                'hourly_views': hourly_views,
                'top_pages_today': [{'page_url': p.page_url, 'views': p.views} for p in top_pages_today],
                'recent_visits': [visit.to_dict() for visit in recent_visits]
            }
            
        except Exception as e:
            logger.error(f"Error getting realtime stats: {str(e)}")
            return {
                'active_sessions': 0,
                'hourly_views': 0,
                'top_pages_today': [],
                'recent_visits': []
            }
    
    @staticmethod
    def generate_export_filename(file_type: str = 'csv') -> str:
        """
        Generate filename for exported statistics
        
        Args:
            file_type: Type of export file (csv, json, etc.)
            
        Returns:
            Generated filename with timestamp
        """
        date_str = datetime.utcnow().strftime('%Y-%m-%d')
        return f"visit-stats-{date_str}.{file_type}"
    
    @staticmethod
    def prepare_csv_export() -> Optional[io.StringIO]:
        """
        Prepare CSV export with proper error handling
        
        Returns:
            StringIO buffer with CSV data or None if failed
        """
        try:
            return StatsService.generate_stats_csv()
        except Exception as e:
            logger.error(f"Error preparing CSV export: {str(e)}")
            return None
