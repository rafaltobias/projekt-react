from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
postgres_user = os.environ.get('POSTGRES_USER', 'postgres')
postgres_host = os.environ.get('POSTGRES_HOST', 'localhost')
postgres_db = os.environ.get('POSTGRES_DB', 'analytics')
postgres_password = os.environ.get('POSTGRES_PASSWORD', 'tobias')
postgres_port = os.environ.get('POSTGRES_PORT', '6666')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

db = SQLAlchemy(app)

# Database Models
class Visit(db.Model):
    __tablename__ = 'visits'
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    page_url = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    referrer = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'page_url': self.page_url,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'country': self.country,
            'city': self.city,
            'referrer': self.referrer
        }

# API Routes
@app.route('/api/visits', methods=['GET'])
def get_visits():
    """Get all visits with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    visits = Visit.query.order_by(Visit.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'visits': [visit.to_dict() for visit in visits.items],
        'total': visits.total,
        'pages': visits.pages,
        'current_page': page
    })

@app.route('/api/visits', methods=['POST'])
def create_visit():
    """Create a new visit record"""
    data = request.get_json()
    
    visit = Visit(
        ip_address=data.get('ip_address'),
        user_agent=data.get('user_agent'),
        page_url=data.get('page_url'),
        country=data.get('country'),
        city=data.get('city'),
        referrer=data.get('referrer')
    )
    
    db.session.add(visit)
    db.session.commit()
    
    return jsonify(visit.to_dict()), 201

@app.route('/api/visits/<int:visit_id>', methods=['GET'])
def get_visit(visit_id):
    """Get a specific visit by ID"""
    visit = Visit.query.get_or_404(visit_id)
    return jsonify(visit.to_dict())

@app.route('/api/visits/<int:visit_id>', methods=['DELETE'])
def delete_visit(visit_id):
    """Delete a visit by ID"""
    visit = Visit.query.get_or_404(visit_id)
    db.session.delete(visit)
    db.session.commit()
    return jsonify({'message': 'Visit deleted successfully'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get basic statistics"""
    total_visits = Visit.query.count()
    unique_ips = db.session.query(Visit.ip_address).distinct().count()
    
    # Get top countries
    top_countries = db.session.query(
        Visit.country, 
        db.func.count(Visit.id).label('count')
    ).filter(Visit.country.isnot(None)).group_by(Visit.country).order_by(
        db.desc('count')
    ).limit(5).all()
    
    # Get recent visits count (last 24 hours)
    from datetime import datetime, timedelta
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_visits = Visit.query.filter(Visit.timestamp >= yesterday).count()
    
    return jsonify({
        'total_visits': total_visits,
        'unique_ips': unique_ips,
        'recent_visits': recent_visits,
        'top_countries': [{'country': country, 'count': count} for country, count in top_countries]
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
