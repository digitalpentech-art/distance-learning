from extensions import celery
from app.services.ai_service import (
    generate_course_outline, 
    generate_quiz_questions, 
    generate_exam_questions
)

@celery.task
def generate_course_task(course_data):
    # Call specialized service
    content = generate_course_outline(
        course_name=course_data.get('course_name'),
        level=course_data.get('level'),
        semester=course_data.get('semester'),
        num_topics=course_data.get('num_topics'),
        difficulty=course_data.get('difficulty')
    )
    
    # In a real app, you would parse the Markdown and save it to the database here
    print(f"Generated Course Content: {content}")
    return "Course structure generated successfully."

@celery.task
def generate_quiz_task(quiz_data):
    # Call specialized service
    content = generate_quiz_questions(
        topic=quiz_data.get('topic'),
        num_questions=quiz_data.get('number_of_questions'),
        difficulty=quiz_data.get('difficulty')
    )
    
    # In a real app, you would parse the output and save it to the database here
    print(f"Generated Quiz: {content}")
    return "Quiz generated successfully."

@celery.task
def generate_exam_task(exam_data):
    # Call specialized service
    content = generate_exam_questions(
        course_name=exam_data.get('course_name'),
        exam_type=exam_data.get('type'),
        difficulty=exam_data.get('difficulty')
    )
    
    # In a real app, you would parse the output and save it to the database here
    print(f"Generated Exam: {content}")
    return "Exam generated successfully."
