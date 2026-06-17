from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import assignment
from app.models.assignment import Assignment, Submission
from extensions import db
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/uploads'

@assignment.route('/course/<int:course_id>/create', methods=['GET', 'POST'])
@login_required
def create_assignment(course_id):
    # Add authorization check (lecturer only) here
    if request.method == 'POST':
        new_assignment = Assignment(
            title=request.form.get('title'),
            description=request.form.get('description'),
            course_id=course_id,
            due_date=request.form.get('due_date') # Needs datetime parsing
        )
        db.session.add(new_assignment)
        db.session.commit()
        flash('Assignment created')
        return redirect(url_for('course.view_course', course_id=course_id))
    return render_template('assignment/create.html', course_id=course_id)

@assignment.route('/<int:assignment_id>/submit', methods=['GET', 'POST'])
@login_required
def submit_assignment(assignment_id):
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            new_submission = Submission(
                assignment_id=assignment_id,
                student_id=current_user.id,
                file_path=file_path
            )
            db.session.add(new_submission)
            db.session.commit()
            flash('Assignment submitted')
            return redirect(url_for('assignment.list_submissions', assignment_id=assignment_id))
    return render_template('assignment/submit.html', assignment_id=assignment_id)
