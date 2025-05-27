from models.database import execute_query
import json

def create_tag(name, description=None, type=None, trigger=None, config=None):
    """Create a new tag"""
    query = """
    INSERT INTO tags (name, description, type, trigger, config)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    """
    # Convert config dict to JSON string if needed
    config_json = json.dumps(config) if config and isinstance(config, dict) else config
    params = (name, description, type, trigger, config_json)
    result = execute_query(query, params)
    if result:
        return result[0]['id']
    return None

def get_all_tags():
    """Get all tags"""
    query = "SELECT * FROM tags ORDER BY name;"
    result = execute_query(query)
    # Make sure we return a list of dictionaries that can be serialized to JSON
    return [dict(row) for row in result] if result else []

def get_tag_by_id(tag_id):
    """Get tag by ID"""
    query = "SELECT * FROM tags WHERE id = %s;"
    params = (tag_id,)
    result = execute_query(query, params)
    return result[0] if result else None

def delete_tag(tag_id):
    """Delete a tag"""
    # First update any visits to set tag_id to NULL
    update_query = "UPDATE visits SET tag_id = NULL WHERE tag_id = %s;"
    execute_query(update_query, (tag_id,))
    
    # Then delete the tag
    query = "DELETE FROM tags WHERE id = %s RETURNING id;"
    params = (tag_id,)
    result = execute_query(query, params)
    return result is not None
