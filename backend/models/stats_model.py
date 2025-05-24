from models.database import execute_query
from datetime import datetime, timedelta
import csv
import io
import logging

def get_visit_stats():
    """Get statistics about visits"""
    # Total visits
    total_query = "SELECT COUNT(*) as total FROM visits;"
    total_result = execute_query(total_query)
    total = total_result[0]['total'] if total_result else 0
    
    # Visits by date (last 30 days)
    by_date_query = """
    SELECT DATE(timestamp) as date, COUNT(*) as count
    FROM visits
    WHERE timestamp > NOW() - INTERVAL '30 days'
    GROUP BY DATE(timestamp)
    ORDER BY date DESC;
    """
    by_date = execute_query(by_date_query)
    
    # Top URLs
    top_urls_query = """
    SELECT page_url, COUNT(*) as count
    FROM visits
    GROUP BY page_url
    ORDER BY count DESC
    LIMIT 10;
    """
    top_urls = execute_query(top_urls_query)
    
    # Top referrers
    top_referrers_query = """
    SELECT referrer, COUNT(*) as count
    FROM visits
    WHERE referrer IS NOT NULL AND referrer != ''
    GROUP BY referrer
    ORDER BY count DESC
    LIMIT 10;
    """
    top_referrers = execute_query(top_referrers_query)
      # Top browsers
    top_browsers_query = """
    SELECT browser, COUNT(*) as count
    FROM visits
    WHERE browser IS NOT NULL
    GROUP BY browser
    ORDER BY count DESC
    LIMIT 5;
    """
    top_browsers = execute_query(top_browsers_query)
    
    # Top operating systems
    top_os_query = """
    SELECT os, COUNT(*) as count
    FROM visits
    WHERE os IS NOT NULL
    GROUP BY os
    ORDER BY count DESC
    LIMIT 5;
    """
    top_os = execute_query(top_os_query)
    
    # Top devices
    top_devices_query = """
    SELECT device, COUNT(*) as count
    FROM visits
    WHERE device IS NOT NULL
    GROUP BY device
    ORDER BY count DESC
    LIMIT 5;
    """
    top_devices = execute_query(top_devices_query)
    
    # Top countries
    top_countries_query = """
    SELECT country, COUNT(*) as count
    FROM visits
    WHERE country IS NOT NULL
    GROUP BY country
    ORDER BY count DESC
    LIMIT 10;
    """
    top_countries = execute_query(top_countries_query)
    
    return {
        'total': total,
        'by_date': by_date,
        'top_urls': top_urls,
        'top_referrers': top_referrers,
        'top_browsers': top_browsers,
        'top_os': top_os,
        'top_devices': top_devices,
        'top_countries': top_countries
    }

def generate_stats_csv():
    """Generate CSV file with visit statistics"""
    query = """
    SELECT id, timestamp, page_url, referrer, user_agent, ip_address, 
           browser, os, device, country, session_id, 
           is_entry_page, is_exit_page
    FROM visits
    ORDER BY timestamp DESC;
    """
    visits = execute_query(query)
    
    if not visits:
        return None
        
    # Create in-memory CSV file
    output = io.StringIO()
    fieldnames = ['id', 'timestamp', 'page_url', 'referrer', 'user_agent', 'ip_address',
                 'browser', 'os', 'device', 'country', 'session_id', 
                 'is_entry_page', 'is_exit_page']
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    writer.writeheader()
    for visit in visits:
        writer.writerow({
            'id': visit['id'],
            'timestamp': visit['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            'page_url': visit['page_url'],
            'referrer': visit['referrer'],
            'user_agent': visit['user_agent'],
            'ip_address': visit['ip_address'],
            'browser': visit['browser'],
            'os': visit['os'],
            'device': visit['device'],
            'country': visit['country'],
            'session_id': visit['session_id'],
            'is_entry_page': visit['is_entry_page'],
            'is_exit_page': visit['is_exit_page']
        })
        
    output.seek(0)
    return output

def get_comprehensive_visit_stats(days=30):
    """Get comprehensive visit statistics for the dashboard"""
    try:
        # Convert days to integer to ensure it's a valid parameter
        days = int(days)
        
        # Total visits
        total_query = """
        SELECT COUNT(*) as total
        FROM visits
        WHERE timestamp > NOW() - INTERVAL %s DAY;
        """
        total_result = execute_query(total_query, (days,))
        total_visits = total_result[0]['total'] if total_result else 0
        
        # Unique sessions  
        sessions_query = """
        SELECT COUNT(DISTINCT session_id) as unique_sessions
        FROM visits
        WHERE timestamp > NOW() - INTERVAL %s DAY;
        """
        sessions_result = execute_query(sessions_query, (days,))
        unique_sessions = sessions_result[0]['unique_sessions'] if sessions_result else 0
        
        # Average session duration (estimated by time between first and last visit)
        avg_duration_query = """
        SELECT AVG(duration) as avg_duration
        FROM (
            SELECT session_id, 
                   EXTRACT(EPOCH FROM (MAX(timestamp) - MIN(timestamp))) as duration
            FROM visits
            WHERE timestamp > NOW() - INTERVAL %s DAY
            GROUP BY session_id
            HAVING COUNT(*) > 1
        ) session_durations;
        """
        duration_result = execute_query(avg_duration_query, (days,))
        avg_duration = duration_result[0]['avg_duration'] if duration_result and duration_result[0]['avg_duration'] else 0
        
        # Visits by date
        daily_query = """
        SELECT DATE(timestamp) as date, COUNT(*) as visits
        FROM visits
        WHERE timestamp > NOW() - INTERVAL %s DAY
        GROUP BY DATE(timestamp)
        ORDER BY date DESC;
        """
        daily_stats = execute_query(daily_query, (days,))
        
        # Top pages
        top_pages_query = """
        SELECT page_url, COUNT(*) as visits
        FROM visits
        WHERE timestamp > NOW() - INTERVAL %s DAY
        GROUP BY page_url
        ORDER BY visits DESC
        LIMIT 10;
        """
        top_pages = execute_query(top_pages_query, (days,))
        
        # Top referrers
        top_referrers_query = """
        SELECT referrer, COUNT(*) as visits
        FROM visits
        WHERE referrer IS NOT NULL AND referrer != ''
        AND timestamp > NOW() - INTERVAL %s DAY
        GROUP BY referrer
        ORDER BY visits DESC
        LIMIT 10;
        """
        top_referrers = execute_query(top_referrers_query, (days,))
        
        # Browser distribution
        browser_stats_query = """
        SELECT browser, COUNT(*) as visits
        FROM visits
        WHERE browser IS NOT NULL
        AND timestamp > NOW() - INTERVAL %s DAY
        GROUP BY browser
        ORDER BY visits DESC
        LIMIT 10;
        """
        browser_stats = execute_query(browser_stats_query, (days,))
        
        # OS distribution
        os_stats_query = """
        SELECT os, COUNT(*) as visits
        FROM visits
        WHERE os IS NOT NULL
        AND timestamp > NOW() - INTERVAL %s DAY
        GROUP BY os
        ORDER BY visits DESC
        LIMIT 10;
        """
        os_stats = execute_query(os_stats_query, (days,))
        
        # Device distribution
        device_stats_query = """
        SELECT device, COUNT(*) as visits
        FROM visits
        WHERE device IS NOT NULL
        AND timestamp > NOW() - INTERVAL %s DAY
        GROUP BY device
        ORDER BY visits DESC
        LIMIT 10;
        """
        device_stats = execute_query(device_stats_query, (days,))
        
        # Country distribution
        country_stats_query = """
        SELECT country, COUNT(*) as visits
        FROM visits
        WHERE country IS NOT NULL
        AND timestamp > NOW() - INTERVAL %s DAY
        GROUP BY country
        ORDER BY visits DESC
        LIMIT 10;
        """
        country_stats = execute_query(country_stats_query, (days,))
        
        return {
            'total_page_views': total_visits,  # Dashboard expects this field name
            'unique_sessions': unique_sessions,
            'avg_session_duration': round(avg_duration / 60, 2) if avg_duration else 0,  # Convert to minutes
            'daily_stats': daily_stats,
            'top_pages': top_pages,
            'top_referrers': top_referrers,
            'browser_stats': browser_stats,
            'os_stats': os_stats,
            'device_stats': device_stats,
            'country_stats': country_stats
        }
    except Exception as e:
        logging.error(f"Error in get_comprehensive_visit_stats: {str(e)}")
        # Return a minimal valid structure to prevent frontend errors
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

def get_realtime_visit_stats():
    """Get real-time visit statistics"""
    
    # Active sessions (last 30 minutes)
    active_sessions_query = """
    SELECT COUNT(DISTINCT session_id) as active_sessions
    FROM visits
    WHERE timestamp > NOW() - INTERVAL '30 minutes';
    """
    active_result = execute_query(active_sessions_query)
    active_sessions = active_result[0]['active_sessions'] if active_result else 0
    
    # Visits in last hour
    hourly_query = """
    SELECT COUNT(*) as hourly_visits
    FROM visits
    WHERE timestamp > NOW() - INTERVAL '1 hour';
    """
    hourly_result = execute_query(hourly_query)
    hourly_visits = hourly_result[0]['hourly_visits'] if hourly_result else 0
    
    # Most visited page in last hour
    popular_page_query = """
    SELECT page_url, COUNT(*) as visits
    FROM visits
    WHERE timestamp > NOW() - INTERVAL '1 hour'
    GROUP BY page_url
    ORDER BY visits DESC
    LIMIT 1;
    """
    popular_result = execute_query(popular_page_query)
    popular_page = popular_result[0] if popular_result else None
    
    # Recent unique visitors
    recent_visitors_query = """
    SELECT COUNT(DISTINCT ip_address) as recent_visitors
    FROM visits
    WHERE timestamp > NOW() - INTERVAL '1 hour';
    """
    visitors_result = execute_query(recent_visitors_query)
    recent_visitors = visitors_result[0]['recent_visitors'] if visitors_result else 0
    
    return {
        'active_sessions': active_sessions,
        'hourly_views': hourly_visits,  # Dashboard expects this field name
        'popular_page': popular_page,
        'recent_visitors': recent_visitors
    }
