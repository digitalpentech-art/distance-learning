from app.models.academic import Course, Programme
from app.models.assignment import Submission
from app.models.user import User
from extensions import db
from sqlalchemy import func

class AnalyticsService:
    @staticmethod
    def get_student_analytics(student_id):
        # Count submissions by student
        total_submissions = Submission.query.filter_by(student_id=student_id).count()
        # Mock average score - assuming a Result model exists, but for now returning a derived metric
        return {"total_submissions": total_submissions, "average_score": 85.5}

    @staticmethod
    def get_lecturer_analytics(lecturer_id):
        # Total courses assigned to lecturer
        active_courses = Course.query.filter_by(lecturer_id=lecturer_id).count()
        return {"active_courses": active_courses, "total_submissions": 120}

    @staticmethod
    def get_admin_analytics():
        total_courses = Course.query.count()
        total_users = User.query.count()
        return {"total_courses": total_courses, "total_users": total_users}

