from extensions import db

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False) # MCQ, TrueFalse, etc.
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    # Options for MCQ would be stored here or in a separate table, 
    # simplifying for now:
    options = db.Column(db.String(500), nullable=True) 
    answer = db.Column(db.String(255), nullable=False)
