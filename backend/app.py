from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging
from logging.handlers import RotatingFileHandler

# Import configuration
from config import Config

# Create Flask app
app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Configure app
app.config.from_object(Config)

# Configure logging
if not app.debug and not app.testing:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/analytics.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Analytics application startup')

# Initialize extensions
from models.db_instance import db
db.init_app(app)
migrate = Migrate(app, db)

# Configure CORS
CORS(app)

# Configure Flask-RESTX API with Swagger documentation
api = Api(
    app,
    version='1.0',
    title='Analytics Tracking API', 
    description='API for tracking website visits, events, and analytics',
    doc='/swagger/'  # Swagger UI endpoint
)

# Configure rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["100 per 15 minutes"]
)

# Import models to ensure they are registered with SQLAlchemy
from models import db_models

# Import routes
from routes.visit_routes import visit_bp, api as visit_api
from routes.stats_routes import stats_bp, api as stats_api
from routes.tag_routes import tag_bp, api as tag_api
from routes.tracking_routes import tracking_bp, api as tracking_api

# Register blueprints
app.register_blueprint(visit_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(tag_bp)
app.register_blueprint(tracking_bp)

# Add namespaces to main API for Swagger documentation
api.add_namespace(visit_api)
api.add_namespace(stats_api)
api.add_namespace(tag_api)
api.add_namespace(tracking_api)

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
