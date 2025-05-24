from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Import routes
from routes.visit_routes import visit_bp
from routes.stats_routes import stats_bp
from routes.tag_routes import tag_bp

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

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
