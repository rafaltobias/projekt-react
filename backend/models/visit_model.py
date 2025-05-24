from models.database import execute_query

def add_visit(page_url, ip_address, user_agent, referrer, browser=None, os=None, device=None, country=None, session_id=None, is_entry_page=False, is_exit_page=False):
    """Add a new visit to the database"""
    query = """
    INSERT INTO visits (page_url, ip_address, user_agent, referrer, browser, os, device, country, session_id, is_entry_page, is_exit_page)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    params = (page_url, ip_address, user_agent, referrer, browser, os, device, country, session_id, is_entry_page, is_exit_page)
    result = execute_query(query, params)
    if result:
        return result[0]
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
