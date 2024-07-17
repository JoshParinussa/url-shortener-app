from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(main)
    
    return app
