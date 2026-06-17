from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from celery import Celery
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()
bcrypt = Bcrypt()
celery = Celery(__name__)
jwt = JWTManager()

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    socketio.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    # Configure Celery
    celery.conf.update(app.config)
