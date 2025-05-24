from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Import routes
from routes.visit_routes import visit_bp
from routes.stats_routes import stats_bp
from routes.tag_routes import tag_bp
from routes.tracking_routes import tracking_bp

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Configure CORS
CORS(app)

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per 15 minutes"]
)

# Register blueprints
app.register_blueprint(visit_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(tag_bp)
app.register_blueprint(tracking_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files including tracking scripts"""
    # Serve from the frontend static directory if it exists
    frontend_static_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'static')
    if os.path.exists(os.path.join(frontend_static_path, filename)):
        return send_from_directory(frontend_static_path, filename)
    
    # Fallback to backend static directory
    return send_from_directory(app.static_folder, filename)

@app.route('/tracking-example')
def tracking_example():
    """Serve the tracking example page"""
    frontend_public_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public')
    return send_from_directory(frontend_public_path, 'tracking-example.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
