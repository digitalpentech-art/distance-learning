from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import admin
from app.models.user import User
from app.models.course_structure import Course, Session, Semester, Subject
from app.models.academic import Faculty, Department, Programme, Level
from extensions import db
from app.models.role import Role
from app.utils.decorators import admin_required

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Simple data aggregation for the dashboard
    student_count = User.query.filter(User.role.has(name=Role.STUDENT)).count()
    course_count = Course.query.count()
    return render_template('admin/dashboard.html', 
                           student_count=student_count, 
                           course_count=course_count)

@admin.route('/faculties', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_faculties():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            new_faculty = Faculty(name=name)
            db.session.add(new_faculty)
            db.session.commit()
            flash('Faculty added.')
        return redirect(url_for('admin.manage_faculties'))
    faculties = Faculty.query.all()
    return render_template('admin/faculties.html', faculties=faculties)

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_departments():
    if request.method == 'POST':
        name = request.form.get('name')
        faculty_id = request.form.get('faculty_id')
        if name and faculty_id:
            new_dept = Department(name=name, faculty_id=faculty_id)
            db.session.add(new_dept)
            db.session.commit()
            flash('Department added.')
        return redirect(url_for('admin.manage_departments'))
    departments = Department.query.all()
    faculties = Faculty.query.all()
    return render_template('admin/departments.html', departments=departments, faculties=faculties)

@admin.route('/programmes', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_programmes():
    if request.method == 'POST':
        name = request.form.get('name')
        department_id = request.form.get('department_id')
        if name and department_id:
            new_prog = Programme(name=name, department_id=department_id)
            db.session.add(new_prog)
            db.session.commit()
            flash('Programme added.')
        return redirect(url_for('admin.manage_programmes'))
    programmes = Programme.query.all()
    departments = Department.query.all()
    return render_template('admin/programmes.html', programmes=programmes, departments=departments)

@admin.route('/sessions', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_sessions():
    if request.method == 'POST':
        name = request.form.get('name')
        level_id = request.form.get('level_id')
        if name and level_id:
            new_session = Session(name=name, level_id=level_id)
            db.session.add(new_session)
            db.session.commit()
            flash('Session added.')
        return redirect(url_for('admin.manage_sessions'))
    sessions = Session.query.all()
    levels = Level.query.all()
    return render_template('admin/sessions.html', sessions=sessions, levels=levels)

@admin.route('/semesters', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_semesters():
    if request.method == 'POST':
        name = request.form.get('name')
        session_id = request.form.get('session_id')
        if name and session_id:
            new_semester = Semester(name=name, session_id=session_id)
            db.session.add(new_semester)
            db.session.commit()
            flash('Semester added.')
        return redirect(url_for('admin.manage_semesters'))
    semesters = Semester.query.all()
    sessions = Session.query.all()
    return render_template('admin/semesters.html', semesters=semesters, sessions=sessions)

@admin.route('/subjects', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_subjects():
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        programme_id = request.form.get('programme_id')
        if code and name and programme_id:
            new_subject = Subject(code=code, name=name, programme_id=programme_id)
            db.session.add(new_subject)
            db.session.commit()
            flash('Subject added.')
        return redirect(url_for('admin.manage_subjects'))
    subjects = Subject.query.all()
    programmes = Programme.query.all()
    return render_template('admin/subjects.html', subjects=subjects, programmes=programmes)

@admin.route('/courses', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_courses():
    if request.method == 'POST':
        name = request.form.get('name')
        subject_id = request.form.get('subject_id')
        semester_id = request.form.get('semester_id')
        if name and subject_id and semester_id:
            new_course = Course(name=name, subject_id=subject_id, semester_id=semester_id)
            db.session.add(new_course)
            db.session.commit()
            flash('Course added.')
        return redirect(url_for('admin.manage_courses'))
    courses = Course.query.all()
    subjects = Subject.query.all()
    semesters = Semester.query.all()
    return render_template('admin/courses.html', courses=courses, subjects=subjects, semesters=semesters)
@admin.route('/users', methods=['GET'])
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin/users.html', users=users, roles=roles)

@admin.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role_id = request.form.get('role_id')

        if not all([username, email, password, role_id]):
            flash('All fields are required.')
            return redirect(url_for('admin.create_user'))

        role = Role.query.get(role_id)
        if not role:
            flash('Invalid role.')
            return redirect(url_for('admin.create_user'))

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.')
        return redirect(url_for('admin.manage_users'))

    roles = Role.query.all()
    return render_template('admin/create_user.html', roles=roles)

@admin.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')
    return redirect(url_for('admin.manage_users'))

@admin.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_suspended:
        user.activate()
        flash('User activated.')
    else:
        user.suspend()
        flash('User suspended.')
    db.session.commit()
    return redirect(url_for('admin.manage_users'))
