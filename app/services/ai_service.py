import os
import google.generativeai as genai

# Configure API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def generate_course_content(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text
