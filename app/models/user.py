from datetime import datetime
from extensions import db, bcrypt
from flask_login import UserMixin
from app.models.role import Role

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    is_active = db.Column(db.Boolean, default=True)
    is_suspended = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role.name == Role.ADMIN

    def is_lecturer(self):
        return self.role.name == Role.LECTURER

    def is_student(self):
        return self.role.name == Role.STUDENT

    def suspend(self):
        """Suspends the user by setting is_suspended to True and is_active to False."""
        self.is_suspended = True
        self.is_active = False

    def activate(self):
        """Activates the user by setting is_suspended to False and is_active to True."""
        self.is_suspended = False
        self.is_active = True

    def update_role(self, new_role):
        """Updates the user's role."""
        self.role = new_role
