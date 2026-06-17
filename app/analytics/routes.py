from flask import jsonify
from flask_login import login_required, current_user
from . import analytics
from app.services.analytics_service import AnalyticsService

@analytics.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard_data():
    # Basic role-based analytics
    if current_user.role.name == 'student':
        data = AnalyticsService.get_student_analytics(current_user.id)
    elif current_user.role.name == 'lecturer':
        data = AnalyticsService.get_lecturer_analytics(current_user.id)
    else:
        data = AnalyticsService.get_admin_analytics()
        
    return jsonify(data)
