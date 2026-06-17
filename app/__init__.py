from flask import Flask
from config import config
from extensions import init_extensions, login_manager

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    init_extensions(app)

    # User loader
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.course import course as course_blueprint
    app.register_blueprint(course_blueprint, url_prefix='/courses')
    from app.chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint, url_prefix='/chat')
    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    from app.assignment import assignment as assignment_blueprint
    app.register_blueprint(assignment_blueprint, url_prefix='/assignments')
    from app.ai import ai as ai_blueprint
    app.register_blueprint(ai_blueprint, url_prefix='/ai')
    from app.analytics import analytics as analytics_blueprint
    app.register_blueprint(analytics_blueprint, url_prefix='/analytics')

    return app
