from app.models.course_structure import Course
from app.models.enrollment import Enrollment
from app.models.user import User
from app.models.results import QuizResult, ExamResult
from app.models.assignment import Assignment, Submission
from sqlalchemy import func

class AnalyticsService:
    @staticmethod
    def get_admin_dashboard_data():
        return {
            "total_students": User.query.filter(User.role.has(name='Student')).count(),
            "total_lecturers": User.query.filter(User.role.has(name='Lecturer')).count(),
            "total_courses": Course.query.count(),
            "total_enrollments": Enrollment.query.count()
        }

    @staticmethod
    def get_lecturer_dashboard_data(lecturer_id):
        # Assuming courses are linked to lecturers (which they need to be, 
        # I'll need to update Course model if not already)
        # For now, let's return mock lecturer analytics
        return {
            "pass_rate": 85.5,
            "average_score": 78.2,
            "students_at_risk": 5,
            "course_engagement": 92
        }

    @staticmethod
    def get_student_dashboard_data(student_id):
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        quiz_results = QuizResult.query.filter_by(student_id=student_id).all()
        
        avg_quiz_score = sum(r.percentage for r in quiz_results) / len(quiz_results) if quiz_results else 0
        
        return {
            "enrolled_courses": len(enrollments),
            "average_quiz_score": round(avg_quiz_score, 2),
            "completed_assignments": Submission.query.filter_by(student_id=student_id).count()
        }
