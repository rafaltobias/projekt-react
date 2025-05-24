from models.database import execute_query
import json

def add_visit(page_url, ip_address, user_agent, referrer, browser=None, os=None, 
              device=None, country=None, session_id=None, is_entry_page=False, 
              is_exit_page=False, event_name=None, event_data=None):
    """Add a new visit to the database"""
    query = """
    INSERT INTO visits (
        page_url, ip_address, user_agent, referrer, browser, os, device, 
        country, session_id, is_entry_page, is_exit_page, event_name, event_data
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    
    # Convert event_data dict to JSON string if it exists
    event_data_json = json.dumps(event_data) if event_data else None
    
    params = (
        page_url, ip_address, user_agent, referrer, browser, os, device,
        country, session_id, is_entry_page, is_exit_page, event_name, event_data_json
    )
    
    result = execute_query(query, params)
    if result:
        return result[0]['id']
    return None

def get_visits(limit=100, offset=0):
    """Get visits from the database"""
    query = """
    SELECT *
    FROM visits
    ORDER BY timestamp DESC
    LIMIT %s OFFSET %s;
    """
    params = (limit, offset)
        
    return execute_query(query, params)

def get_visit_count():
    """Get the total count of visits"""
    query = "SELECT COUNT(*) as count FROM visits;"
    result = execute_query(query)
    return result[0]['count'] if result else 0

def get_visits_by_session(session_id, limit=100):
    """Get all visits for a specific session"""
    query = """
    SELECT *
    FROM visits
    WHERE session_id = %s
    ORDER BY timestamp ASC
    LIMIT %s;
    """
    params = (session_id, limit)
    return execute_query(query, params)

def get_unique_sessions_count(days=30):
    """Get count of unique sessions within the specified timeframe"""
    query = """
    SELECT COUNT(DISTINCT session_id) as count
    FROM visits
    WHERE timestamp > NOW() - INTERVAL %s DAY;
    """
    params = (days,)
    result = execute_query(query, params)
    return result[0]['count'] if result else 0

def update_exit_pages(session_id, new_visit_id):
    """Update previous visits in the session to not be exit pages"""
    query = """
    UPDATE visits
    SET is_exit_page = FALSE
    WHERE session_id = %s AND id != %s;
    """
    params = (session_id, new_visit_id)
    execute_query(query, params)
    return True
