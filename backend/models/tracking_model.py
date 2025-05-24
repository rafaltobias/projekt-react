from models.database import execute_query
import json
from datetime import datetime, timedelta

def add_tracking_event(session_id, page_url, ip_address, user_agent, referrer=None, 
                      browser=None, os=None, device=None, country=None, city=None,
                      is_entry_page=False, is_exit_page=False, event_name=None, event_data=None):
    """Add a new tracking event to the database"""
    query = """
    INSERT INTO tracking_events (
        session_id, page_url, ip_address, user_agent, referrer, browser, os, device, 
        country, city, is_entry_page, is_exit_page, event_name, event_data
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id, timestamp;
    """
    
    # Convert event_data dict to JSON if it exists
    event_data_json = json.dumps(event_data) if event_data else None
    
    params = (
        session_id, page_url, ip_address, user_agent, referrer, browser, os, device,
        country, city, is_entry_page, is_exit_page, event_name, event_data_json
    )
    
    result = execute_query(query, params)
    if result:
        return {
            'id': result[0]['id'],
            'timestamp': result[0]['timestamp']
        }
    return None

def get_tracking_events(limit=100, offset=0):
    """Get tracking events from the database"""
    query = """
    SELECT *
    FROM tracking_events
    ORDER BY timestamp DESC
    LIMIT %s OFFSET %s;
    """
    params = (limit, offset)
    return execute_query(query, params)

def get_page_views(limit=100, offset=0):
    """Get page views (excluding custom events)"""
    query = """
    SELECT *
    FROM page_views
    ORDER BY timestamp DESC
    LIMIT %s OFFSET %s;
    """
    params = (limit, offset)
    return execute_query(query, params)

def get_custom_events(limit=100, offset=0):
    """Get custom events only"""
    query = """
    SELECT *
    FROM custom_events
    ORDER BY timestamp DESC
    LIMIT %s OFFSET %s;
    """
    params = (limit, offset)
    return execute_query(query, params)

def get_session_data(session_id):
    """Get all tracking events for a specific session"""
    query = """
    SELECT *
    FROM tracking_events
    WHERE session_id = %s
    ORDER BY timestamp ASC;
    """
    params = (session_id,)
    return execute_query(query, params)

def get_session_analytics(session_id=None):
    """Get session analytics data"""
    if session_id:
        query = """
        SELECT *
        FROM session_analytics
        WHERE session_id = %s;
        """
        params = (session_id,)
    else:
        query = """
        SELECT *
        FROM session_analytics
        ORDER BY session_start DESC
        LIMIT 100;
        """
        params = ()
    
    return execute_query(query, params)

def get_tracking_stats(days=30):
    """Get comprehensive tracking statistics"""
    
    # Total page views
    total_query = """
    SELECT COUNT(*) as total
    FROM tracking_events
    WHERE (event_name IS NULL OR event_name = 'page_view')
    AND timestamp > CURRENT_TIMESTAMP - INTERVAL '%s days';
    """
    total_result = execute_query(total_query, (days,))
    total_page_views = total_result[0]['total'] if total_result else 0
    
    # Unique sessions
    sessions_query = """
    SELECT COUNT(DISTINCT session_id) as unique_sessions
    FROM tracking_events
    WHERE timestamp > CURRENT_TIMESTAMP - INTERVAL '%s days';
    """
    sessions_result = execute_query(sessions_query, (days,))
    unique_sessions = sessions_result[0]['unique_sessions'] if sessions_result else 0
    
    # Page views by date
    daily_query = """
    SELECT DATE(timestamp) as date, COUNT(*) as page_views
    FROM tracking_events
    WHERE (event_name IS NULL OR event_name = 'page_view')
    AND timestamp > CURRENT_TIMESTAMP - INTERVAL '%s days'
    GROUP BY DATE(timestamp)
    ORDER BY date DESC;
    """
    daily_stats = execute_query(daily_query, (days,))
    
    # Top pages
    top_pages_query = """
    SELECT page_url, COUNT(*) as views
    FROM tracking_events
    WHERE (event_name IS NULL OR event_name = 'page_view')
    AND timestamp > CURRENT_TIMESTAMP - INTERVAL '%s days'
    GROUP BY page_url
    ORDER BY views DESC
    LIMIT 10;
    """
    top_pages = execute_query(top_pages_query, (days,))
      # Top referrers
    top_referrers_query = """
    SELECT referrer, COUNT(*) as count
    FROM tracking_events
    WHERE referrer IS NOT NULL AND referrer != ''
    AND timestamp > CURRENT_TIMESTAMP - INTERVAL '%s days'
    GROUP BY referrer
    ORDER BY count DESC
    LIMIT 10;
    """
    top_referrers = execute_query(top_referrers_query, (days,))
    
    # Browser stats
    browser_stats_query = """
    SELECT browser, COUNT(*) as count
    FROM tracking_events
    WHERE browser IS NOT NULL
    AND timestamp > CURRENT_TIMESTAMP - INTERVAL '%s days'
    GROUP BY browser
    ORDER BY count DESC
    LIMIT 10;
    """
    browser_stats = execute_query(browser_stats_query, (days,))
    
    # OS stats
    os_stats_query = """
    SELECT os, COUNT(*) as count
    FROM tracking_events
    WHERE os IS NOT NULL
    AND timestamp > CURRENT_TIMESTAMP - INTERVAL '%s days'
    GROUP BY os
    ORDER BY count DESC
    LIMIT 10;
    """
    os_stats = execute_query(os_stats_query, (days,))
    
    # Device stats
    device_stats_query = """
    SELECT device, COUNT(*) as count
    FROM tracking_events
    WHERE device IS NOT NULL
    AND timestamp > CURRENT_TIMESTAMP - INTERVAL '%s days'
    GROUP BY device
    ORDER BY count DESC
    LIMIT 5;
    """
    device_stats = execute_query(device_stats_query, (days,))
    
    # Country stats
    country_stats_query = """
    SELECT country, COUNT(*) as count
    FROM tracking_events
    WHERE country IS NOT NULL
    AND timestamp > CURRENT_TIMESTAMP - INTERVAL '%s days'
    GROUP BY country
    ORDER BY count DESC
    LIMIT 10;
    """
    country_stats = execute_query(country_stats_query, (days,))
      # Custom events stats
    events_stats_query = """
    SELECT event_name, COUNT(*) as count
    FROM tracking_events
    WHERE event_name IS NOT NULL AND event_name != 'page_view'
    AND timestamp > CURRENT_TIMESTAMP - INTERVAL '%s days'
    GROUP BY event_name
    ORDER BY count DESC
    LIMIT 10;
    """
    events_stats = execute_query(events_stats_query, (days,))
    
    return {
        'total_page_views': total_page_views,
        'unique_sessions': unique_sessions,
        'daily_stats': daily_stats,
        'top_pages': top_pages,
        'top_referrers': top_referrers,
        'browser_stats': browser_stats,
        'os_stats': os_stats,
        'device_stats': device_stats,
        'country_stats': country_stats,
        'events_stats': events_stats
    }

def update_exit_pages(session_id, current_event_id):
    """Update previous events in the session to not be exit pages"""
    query = """
    UPDATE tracking_events
    SET is_exit_page = FALSE
    WHERE session_id = %s AND id != %s;
    """
    params = (session_id, current_event_id)
    execute_query(query, params)
    return True

def get_real_time_stats():
    """Get real-time statistics for dashboard"""
    # Active sessions (last 30 minutes)
    active_sessions_query = """
    SELECT COUNT(DISTINCT session_id) as active_sessions
    FROM tracking_events
    WHERE timestamp > CURRENT_TIMESTAMP - INTERVAL '30 minutes';
    """
    active_result = execute_query(active_sessions_query)
    active_sessions = active_result[0]['active_sessions'] if active_result else 0
    
    # Page views in last hour
    hourly_query = """
    SELECT COUNT(*) as hourly_views
    FROM tracking_events
    WHERE (event_name IS NULL OR event_name = 'page_view')
    AND timestamp > CURRENT_TIMESTAMP - INTERVAL '1 hour';
    """
    hourly_result = execute_query(hourly_query)
    hourly_views = hourly_result[0]['hourly_views'] if hourly_result else 0
    
    # Most viewed page in last hour
    popular_page_query = """
    SELECT page_url, COUNT(*) as views
    FROM tracking_events
    WHERE (event_name IS NULL OR event_name = 'page_view')
    AND timestamp > CURRENT_TIMESTAMP - INTERVAL '1 hour'
    GROUP BY page_url
    ORDER BY views DESC
    LIMIT 1;
    """
    popular_result = execute_query(popular_page_query)
    popular_page = popular_result[0] if popular_result else None
    
    return {
        'active_sessions': active_sessions,
        'hourly_views': hourly_views,
        'popular_page': popular_page
    }
