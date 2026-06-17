import os
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from . import course
from app.models.course_structure import Course
from app.models.lesson_structure import Topic, Lesson, Content
from app.models.quiz_structure import Quiz, Question
from extensions import db
from app.utils.decorators import lecturer_required

@course.route('/<int:course_id>/add-quiz', methods=['GET', 'POST'])
@login_required
@lecturer_required
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
@login_required
@lecturer_required
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
@login_required
@lecturer_required
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
@login_required
@lecturer_required
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
@login_required
@lecturer_required
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

@course.route('/lesson/<int:lesson_id>/add-content', methods=['GET', 'POST'])
@login_required
@lecturer_required
def add_content(lesson_id):
    if request.method == 'POST':
        title = request.form.get('title')
        content_type = request.form.get('type')

        url = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                filename = secure_filename(file.filename)
                upload_folder = os.path.join(current_app.root_path, 'uploads', content_type.lower() + 's')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file.save(os.path.join(upload_folder, filename))
                url = os.path.join(content_type.lower() + 's', filename)
        else:
            url = request.form.get('url')

        new_content = Content(title=title, type=content_type, url=url, lesson_id=lesson_id)
        db.session.add(new_content)
        db.session.commit()
        flash('Content added.')
        lesson = Lesson.query.get(lesson_id)
        return redirect(url_for('course.view_course', course_id=lesson.topic.course_id))
    return render_template('course/add_content.html', lesson_id=lesson_id)

@course.route('/quiz/<int:quiz_id>')
@login_required
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('course/quiz.html', quiz=quiz)

@course.route('/quiz/<int:quiz_id>/grade', methods=['POST'])
@login_required
def grade_quiz(quiz_id):
    from app.services.quiz_service import QuizService
    from app.models.user import User

    answers = request.form.to_dict()
    result = QuizService.grade_quiz(quiz_id, current_user.id, answers)

    flash(f'Quiz submitted! Score: {result.percentage:.2f}%')
    return redirect(url_for('course.view_course', course_id=result.quiz.course_id))


