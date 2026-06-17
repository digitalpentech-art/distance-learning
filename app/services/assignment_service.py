from datetime import datetime
from extensions import db
from app.models.assignment import Assignment, Submission

class AssignmentService:
    @staticmethod
    def create_assignment(course_id, title, description, due_date_str):
        """Creates a new assignment."""
        due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
        new_assignment = Assignment(
            title=title,
            description=description,
            course_id=course_id,
            due_date=due_date
        )
        db.session.add(new_assignment)
        db.session.commit()
        return new_assignment

    @staticmethod
    def submit_assignment(assignment_id, student_id, file_path):
        """Creates a new submission for an assignment."""
        new_submission = Submission(
            assignment_id=assignment_id,
            student_id=student_id,
            file_path=file_path
        )
        db.session.add(new_submission)
        db.session.commit()
        return new_submission

    @staticmethod
    def grade_submission(submission_id, grade, remarks):
        """Grades an existing submission."""
        submission = Submission.query.get_or_404(submission_id)
        submission.grade = grade
        submission.remarks = remarks
        db.session.commit()
        return submission
