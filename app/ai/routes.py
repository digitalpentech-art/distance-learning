from flask import request, jsonify
from . import ai
from .tasks import generate_course_task, generate_quiz_task, generate_exam_task
from flask_login import login_required, current_user
from app.services.ai_service import generate_course_content
from app.models.assignment import Submission # Placeholder for recommendation logic

@ai.route('/tutor', methods=['POST'])
@login_required
def ai_tutor():
    data = request.get_json()
    prompt = f"Explain the following concept to a student: {data.get('question')}"
    response = generate_course_content(prompt)
    return jsonify({"response": response}), 200

@ai.route('/generate-quiz', methods=['POST'])
@login_required
def generate_quiz():
    data = request.get_json()
    generate_quiz_task.delay(data)
    return jsonify({"msg": "Quiz generation task started"}), 202

@ai.route('/generate-exam', methods=['POST'])
@login_required
def generate_exam():
    data = request.get_json()
    generate_exam_task.delay(data)
    return jsonify({"msg": "Exam generation task started"}), 202

@ai.route('/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    # Placeholder logic: Analyze student submissions/results
    # Here we would query the database for user performance
    # For now, just generate a generic recommendation based on a mock prompt
    prompt = f"Provide study recommendations for a student who is struggling with course topics."
    response = generate_course_content(prompt)
    return jsonify({"recommendations": response}), 200

