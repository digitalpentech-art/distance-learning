from extensions import celery
from app.services.ai_service import generate_course_content

@celery.task
def generate_course_task(course_data):
    # Construct a prompt based on course_data
    prompt = f"Create a course outline for: {course_data.get('course_name')}, Level: {course_data.get('level')}, Difficulty: {course_data.get('difficulty')}"
    
    # Call Gemini API
    content = generate_course_content(prompt)
    
    # In a real app, you would save this content to the database here
    print(f"Generated Content: {content}")
    return "Course structure generated successfully."

@celery.task
def generate_quiz_task(quiz_data):
    # Construct a prompt for quiz generation
    prompt = f"Create a {quiz_data.get('number_of_questions')} question quiz on {quiz_data.get('topic')} with difficulty {quiz_data.get('difficulty')}. Return in JSON format."
    
    # Call Gemini API
    content = generate_course_content(prompt)
    
    # In a real app, you would save this quiz to the database here
    print(f"Generated Quiz: {content}")
    return "Quiz generated successfully."

@celery.task
def generate_exam_task(exam_data):
    # Construct a prompt for exam generation
    prompt = f"Create a {exam_data.get('type')} exam for {exam_data.get('course_name')}. Include questions, answers, and a marking guide. Format as structured text."
    
    # Call Gemini API
    content = generate_course_content(prompt)
    
    # In a real app, you would save this exam to the database here
    print(f"Generated Exam: {content}")
    return "Exam generated successfully."
