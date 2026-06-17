from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import student
from app.models.course_structure import Course
from app.models.enrollment import Enrollment
from extensions import db

@student.route('/')
@login_required
def dashboard():
    """Student dashboard: shows enrolled courses and recent activities."""
    enrolled_courses = Enrollment.query.filter_by(student_id=current_user.id, is_active=True).all()
    # In a real app, we'd also fetch recent notifications, recommendations, etc.
    return render_template('student/dashboard.html', enrollments=enrolled_courses)

@student.route('/courses')
@login_required
def list_available_courses():
    """Lists all courses available for enrollment."""
    all_courses = Course.query.all()
    # In a real app, we'd filter out courses the student is already enrolled in
    already_enrolled_ids = [e.course_id for e in current_user.enrollments if e.is_active]
    available_courses = [c for c in all_courses if c.id not in already_enrolled_ids]
    return render_template('student/available_courses.html', courses=available_courses)

@student.route('/courses/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll(course_id):
    """Handles course enrollment."""
    # Check if already enrolled
    existing_enrollment = Enrollment.query.filter_by(
        student_id=current_user.id, 
        course_id=course_id, 
        is_active=True
    ).first()

    if existing_enrollment:
        flash('You are already enrolled in this course.')
        return redirect(url_for('student.list_available_courses'))

    new_enrollment = Enrollment(student_id=current_user.id, course_id=course_id)
    db.session.add(new_enrollment)
    db.session.commit()
    flash('Successfully enrolled in the course!')
    return redirect(url_for('student.dashboard'))

@student.route('/course/<int:course_id>')
@login_required
def view_course(course_id):
    """Student view of a course: topics and lessons."""
    course = Course.query.get_or_404(course_id)
    
    # Verify enrollment
    is_enrolled = Enrollment.query.filter_by(
        student_id=current_user.id, 
        course_id=course_id, 
        is_active=True
    ).first()

    if not is_enrolled:
        flash('You must enroll in this course to view its content.')
        return redirect(url_for('student.list_available_courses'))

    return render_template('student/course_view.html', course=course)
