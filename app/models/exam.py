from extensions import db

class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False) # Mid, Final, Mock
    questions = db.relationship('Question', backref='exam', lazy=True)

class ExamQuestion(db.Model):
    __tablename__ = 'exam_questions'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
