from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.database import db
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
postgres_db = os.environ.get('POSTGRES_DB', 'analytics')
postgres_password = os.environ.get('POSTGRES_PASSWORD', 'tobias')
postgres_port = os.environ.get('POSTGRES_PORT', '6666')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Initialize extensions
db.init_app(app)
CORS(app)

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["100 per 15 minutes"]
)

# Import models first to ensure they're registered with SQLAlchemy
from src.models.models import Visit, Tag, StatsView

# Import blueprints after db initialization to avoid circular imports
from src.routes.visit_routes import visit_bp
from src.routes.stats_routes import stats_bp
from src.routes.tag_routes import tag_bp

# Register blueprints
app.register_blueprint(visit_bp, url_prefix='/api')
app.register_blueprint(stats_bp, url_prefix='/api')
app.register_blueprint(tag_bp, url_prefix='/api')

# Add health check endpoint
@app.route('/api/health')
def health_check():
    try:
        # Check database connection
        db_ok = False
        tables_count = 0
        error_msg = None
        try:
            # Execute a simple query to check DB connection
            tables_count = db.session.execute(db.text("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'")).scalar()
            db_ok = True
        except Exception as e:
            error_msg = str(e)
            
        return jsonify({
            'status': 'ok', 
            'message': 'Server is running',
            'database': {
                'connected': db_ok,
                'tables_count': tables_count,
                'error': error_msg
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error in health check: {str(e)}'
        })

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)