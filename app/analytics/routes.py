from flask import render_template
from flask_login import login_required, current_user
from . import analytics
from app.services.analytics_service import AnalyticsService

@analytics.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        data = AnalyticsService.get_admin_dashboard_data()
        return render_template('analytics/admin_dashboard.html', data=data)
    elif current_user.is_lecturer():
        data = AnalyticsService.get_lecturer_dashboard_data(current_user.id)
        return render_template('analytics/lecturer_dashboard.html', data=data)
    else:
        data = AnalyticsService.get_student_dashboard_data(current_user.id)
        return render_template('analytics/student_dashboard.html', data=data)
