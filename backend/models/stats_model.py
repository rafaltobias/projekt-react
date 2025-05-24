from models.database import execute_query
from datetime import datetime, timedelta
import csv
import io

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
