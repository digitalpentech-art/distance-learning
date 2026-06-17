from extensions import db

class Faculty(db.Model):
    __tablename__ = 'faculties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    departments = db.relationship('Department', backref='faculty', lazy=True)

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    programmes = db.relationship('Programme', backref='department', lazy=True)

class Programme(db.Model):
    __tablename__ = 'programmes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    levels = db.relationship('Level', backref='programme', lazy=True)

class Level(db.Model):
    __tablename__ = 'levels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False) # e.g., 100, 200
    programme_id = db.Column(db.Integer, db.ForeignKey('programmes.id'), nullable=False)
    sessions = db.relationship('Session', backref='level', lazy=True)
