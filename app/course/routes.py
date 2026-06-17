from flask import render_template, redirect, url_for, flash, request
from . import course
from app.models.course_structure import Course
from app.models.lesson_structure import Topic, Lesson, Content
from app.models.quiz_structure import Quiz, Question

@course.route('/<int:course_id>/add-quiz', methods=['GET', 'POST'])
def add_quiz(course_id):
    if request.method == 'POST':
        new_quiz = Quiz(
            title=request.form.get('title'),
            course_id=course_id
        )
        db.session.add(new_quiz)
        db.session.commit()
        flash('Quiz added')
        return redirect(url_for('course.view_course', course_id=course_id))
    return render_template('course/add_quiz.html', course_id=course_id)

@course.route('/quiz/<int:quiz_id>/add-question', methods=['GET', 'POST'])
def add_question(quiz_id):
    if request.method == 'POST':
        new_question = Question(
            text=request.form.get('text'),
            type=request.form.get('type'),
            answer=request.form.get('answer'),
            options=request.form.get('options'),
            quiz_id=quiz_id
        )
        db.session.add(new_question)
        db.session.commit()
        flash('Question added')
        quiz = Quiz.query.get(quiz_id)
        return redirect(url_for('course.view_course', course_id=quiz.course_id))
    return render_template('course/add_question.html', quiz_id=quiz_id)
from extensions import db

@course.route('/')
def list_courses():
    courses = Course.query.all()
    return render_template('course/list.html', courses=courses)

@course.route('/create', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        new_course = Course(
            name=request.form.get('name'),
            subject_id=request.form.get('subject_id'),
            semester_id=request.form.get('semester_id')
        )
        db.session.add(new_course)
        db.session.commit()
        flash('Course created')
        return redirect(url_for('course.list_courses'))
    return render_template('course/create.html')

@course.route('/<int:course_id>')
def view_course(course_id):
    course_obj = Course.query.get_or_404(course_id)
    topics = Topic.query.filter_by(course_id=course_id).all()
    return render_template('course/view.html', course=course_obj, topics=topics)

@course.route('/<int:course_id>/add-topic', methods=['GET', 'POST'])
def add_topic(course_id):
    if request.method == 'POST':
        new_topic = Topic(
            name=request.form.get('name'),
            course_id=course_id
        )
        db.session.add(new_topic)
        db.session.commit()
        flash('Topic added')
        return redirect(url_for('course.view_course', course_id=course_id))
    return render_template('course/add_topic.html', course_id=course_id)

@course.route('/topic/<int:topic_id>/add-lesson', methods=['GET', 'POST'])
def add_lesson(topic_id):
    if request.method == 'POST':
        new_lesson = Lesson(
            name=request.form.get('name'),
            topic_id=topic_id
        )
        db.session.add(new_lesson)
        db.session.commit()
        flash('Lesson added')
        topic = Topic.query.get(topic_id)
        return redirect(url_for('course.view_course', course_id=topic.course_id))
    return render_template('course/add_lesson.html', topic_id=topic_id)

@course.route('/quiz/<int:quiz_id>/grade', methods=['POST'])
@login_required
def grade_quiz(quiz_id):
    quiz_obj = Quiz.query.get_or_404(quiz_id)
    score = 0
    total_questions = len(quiz_obj.questions)
    
    for question in quiz_obj.questions:
        student_answer = request.form.get(f'q_{question.id}')
        if student_answer == question.answer:
            score += 1
            
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    flash(f'Quiz submitted! Score: {percentage:.2f}%')
    return redirect(url_for('course.view_course', course_id=quiz_obj.course_id))
