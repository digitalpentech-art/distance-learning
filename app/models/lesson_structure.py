from extensions import db

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    lessons = db.relationship('Lesson', backref='topic', lazy=True)

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    contents = db.relationship('Content', backref='lesson', lazy=True)

class Content(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # PDF, Video, Note
    url = db.Column(db.String(255), nullable=True) # File path or external link
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
