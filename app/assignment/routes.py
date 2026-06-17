from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from . import assignment
from app.models.assignment import Assignment, Submission
from app.services.assignment_service import AssignmentService
from app.utils.decorators import lecturer_required, student_required
from extensions import db
import os
from werkzeug.utils import secure_filename

@assignment.route('/course/<int:course_id>/create', methods=['GET', 'POST'])
@login_required
@lecturer_required
def create_assignment(course_id):
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')

        if not all([title, due_date_str]):
            flash('Title and due date are required.')
            return redirect(url_for('assignment.create_assignment', course_id=course_id))

        try:
            AssignmentService.create_assignment(course_id, title, description, due_date_str)
            flash('Assignment created successfully.')
            return redirect(url_for('course.view_course', course_id=course_id))
        except Exception as e:
            flash(f'Error creating assignment: {str(e)}')
            return redirect(url_for('assignment.create_assignment', course_id=course_id))

    return render_template('assignment/create.html', course_id=course_id)

@assignment.route('/<int:assignment_id>/submit', methods=['GET', 'POST'])
@login_required
@student_required
def submit_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('No file uploaded.')
            return redirect(url_for('assignment.submit_assignment', assignment_id=assignment_id))

        filename = secure_filename(file.filename)
        # Use a safer upload path
        upload_folder = os.path.join(current_app.root_path, 'uploads', 'assignments')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        try:
            AssignmentService.submit_assignment(assignment_id, current_user.id, file_path)
            flash('Assignment submitted successfully.')
            return redirect(url_for('student.dashboard'))
        except Exception as e:
            flash(f'Error submitting assignment: {str(e)}')
            return redirect(url_for('assignment.submit_assignment', assignment_id=assignment_id))

    return render_template('assignment/submit.html', assignment=assignment)

@assignment.route('/<int:assignment_id>/submissions', methods=['GET'])
@login_required
@lecturer_required
def list_submissions(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    submissions = Submission.query.filter_by(assignment_id=assignment_id).all()
    return render_template('assignment/submissions.html', assignment=assignment, submissions=submissions)

@assignment.route('/<int:submission_id>/grade', methods=['GET', 'POST'])
@login_required
@lecturer_required
def grade_submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    
    if request.method == 'POST':
        grade = request.form.get('grade')
        remarks = request.form.get('remarks')
        
        try:
            AssignmentService.grade_submission(submission_id, grade, remarks)
            flash('Submission graded successfully.')
            return redirect(url_for('assignment.list_submissions', assignment_id=submission.assignment_id))
        except Exception as e:
            flash(f'Error grading submission: {str(e)}')
            return redirect(url_for('assignment.grade_submission', submission_id=submission_id))

    return render_template('assignment/grade.html', submission=submission)
