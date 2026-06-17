from datetime import datetime
from extensions import db
from app.models.user import User
from app.models.course_structure import Course

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    reason = db.Column(db.Text, nullable=True) # e.g., "Based on your quiz scores in Machine Learning"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='recommendations', lazy=True)
    course = db.relationship('Course', backref='recommendations', lazy=True)
