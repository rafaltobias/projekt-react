#!/usr/bin/env python3
import sys
sys.path.append('.')

try:
    from routes.tag_routes import tag_bp
    print("SUCCESS: tag_bp imported successfully")
    print(f"tag_bp: {tag_bp}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
