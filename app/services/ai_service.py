import os
import google.generativeai as genai

# Configure API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_course_content(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def generate_recommendations(student_performance_data):
    prompt = f"""
    Act as an expert learning analytics specialist. Based on the following student performance data, provide personalized study recommendations.
    
    Student Data: {student_performance_data}
    
    Your recommendations should include:
    1. Specific topics to focus on (based on weak areas).
    2. Recommended videos or reading materials.
    3. Suggested practice questions or exercises.
    4. Additional notes or resources for improvement.
    
    Provide the output in a clear, actionable, and encouraging Markdown format.
    """
    return generate_course_content(prompt)
