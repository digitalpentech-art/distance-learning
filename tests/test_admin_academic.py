import pytest
from app.models.academic import Faculty, Department
from extensions import db
from app.models.user import User
from app.models.role import Role

def test_faculty_department_crud(app):
    with app.app_context():
        # Setup: Need an admin user
        role = Role(name=Role.ADMIN)
        db.session.add(role)
        db.session.commit()
        admin = User(username='admin', email='admin@test.com', role_id=role.id)
        admin.set_password('password')
        db.session.add(admin)
        db.session.commit()

        # Test Faculty Creation via route
        client = app.test_client()
        with client:
            client.post('/auth/login', data={'username': 'admin', 'password': 'password'})
            
            # Post Faculty
            response = client.post('/admin/faculties', data={'name': 'Science'}, follow_redirects=True)
            assert response.status_code == 200
            assert b'Science' in response.data
            
            faculty = Faculty.query.filter_by(name='Science').first()
            assert faculty is not None
            
            # Post Department
            response = client.post('/admin/departments', 
                                   data={'name': 'Computer Science', 'faculty_id': faculty.id}, 
                                   follow_redirects=True)
            assert response.status_code == 200
            assert b'Computer Science' in response.data
            
            dept = Department.query.filter_by(name='Computer Science').first()
            assert dept is not None
            assert dept.faculty_id == faculty.id
