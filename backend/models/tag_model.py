from models.database import execute_query

def create_tag(name, description=None):
    """Create a new tag"""
    query = """
    INSERT INTO tags (name, description)
    VALUES (%s, %s)
    RETURNING id;
    """
    params = (name, description)
    result = execute_query(query, params)
    if result:
        return result[0]
    return None

def get_all_tags():
    """Get all tags"""
    query = "SELECT * FROM tags ORDER BY name;"
    return execute_query(query)

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
