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
    question = data.get('question')
    # In a real app, we might also pass context like current course or last topic studied
    response = generate_ai_tutor_response(question)
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
    # In a real app, we would query the database for the user's actual performance
    # e.g., quiz scores, exam results, completed topics, etc.
    mock_performance_data = {
        "user_id": current_user.id,
        "username": current_user.username,
        "recent_quiz_scores": [75, 82, 60],
        "weak_topics": ["Neural Networks", "Backpropagation"],
        "completed_topics": ["Linear Regression", "Gradient Descent"]
    }
    
    response = generate_recommendations(str(mock_performance_data))
    return jsonify({"recommendations": response}), 200

