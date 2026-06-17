import pytest
from app.models.user import User
from app.models.role import Role
from extensions import db

def test_user_creation_with_defaults(app):
    with app.app_context():
        # Setup
        role = Role(name=Role.STUDENT)
        db.session.add(role)
        db.session.commit()
        
        user = User(username='testuser', email='test@example.com', role_id=role.id)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        # Assertions
        assert user.is_active is True
        assert user.is_suspended is False
        assert user.created_at is not None
        assert user.is_student() is True

def test_user_status_updates(app):
    with app.app_context():
        # Setup
        role = Role(name=Role.LECTURER)
        db.session.add(role)
        db.session.commit()
        
        user = User(username='lecturer', email='lecturer@example.com', role_id=role.id)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        # Assertions
        user.is_suspended = True
        db.session.commit()
        assert user.is_suspended is True
        
        user.is_active = False
        db.session.commit()
        assert user.is_active is False
