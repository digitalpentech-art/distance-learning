from extensions import db
from datetime import datetime
import uuid

class Certificate(db.Model):
    __tablename__ = 'certificates'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    certificate_number = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4()))
    verification_link = db.Column(db.String(255), nullable=True)
