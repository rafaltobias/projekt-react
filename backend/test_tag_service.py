#!/usr/bin/env python3
"""
Test script to verify tag service functionality
"""
from app import app
from services.tag_service import TagService

def test_tag_service():
    """Test tag service operations"""
    try:
        with app.app_context():
            print("=== Testing Tag Service ===")
            
            # Test get all tags
            tags = TagService.get_all_tags()
            print(f"Found {len(tags) if tags else 0} tags")
            
            if tags:
                # Show first tag
                first_tag = tags[0]
                print(f"First tag: ID={first_tag['id']}, Name={first_tag['name']}")
                
                # Test get tag by id
                tag_detail = TagService.get_tag_by_id(first_tag['id'])
                if tag_detail:
                    print(f"Tag detail: {tag_detail['name']} - {tag_detail.get('description', 'No description')}")
                else:
                    print("Failed to get tag by ID")
            
            print("✅ Tag service test completed successfully")
            
    except Exception as e:
        print(f"❌ Tag service test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_tag_service()
