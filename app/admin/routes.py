from flask import render_template
from . import admin
from app.models.user import User
from app.models.course_structure import Course

@admin.route('/dashboard')
def dashboard():
    # Simple data aggregation for the dashboard
    student_count = User.query.filter_by(role_id=1).count() # Assuming role_id 1 is student
    course_count = Course.query.count()
    return render_template('admin/dashboard.html', 
                           student_count=student_count, 
                           course_count=course_count)
