import unittest.mock as mock
from app.services.ai_service import generate_course_content

@mock.patch('google.generativeai.GenerativeModel.generate_content')
def test_ai_service_generation(mock_generate):
    # Mock the API response
    mock_response = mock.Mock()
    mock_response.text = "Mocked Course Outline"
    mock_generate.return_value = mock_response
    
    result = generate_course_content("Generate course for Math")
    
    assert result == "Mocked Course Outline"
    mock_generate.assert_called_once()
