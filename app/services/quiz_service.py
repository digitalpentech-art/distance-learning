from extensions import db
from app.models.quiz_structure import Quiz, Question, QuizResult
from app.models.user import User

class QuizService:
    @staticmethod
    def grade_quiz(quiz_id, student_id, answers):
        """
        Grades a submitted quiz.
        :param quiz_id: ID of the quiz being graded
        :param student_id: ID of the student who submitted it
        :param answers: Dictionary of {question_id: student_answer}
        :return: The QuizResult object
        """
        quiz = Quiz.query.get_or_404(quiz_id)
        questions = quiz.questions
        score = 0
        total_questions = len(questions)

        for question in questions:
            student_answer = answers.get(str(question.id))
            if student_answer:
                # Simple string comparison for now. 
                # In a real app, we'd handle case-insensitivity, trimming, etc.
                if str(student_answer).strip().lower() == str(question.answer).strip().lower():
                    score += 1

        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        result = QuizResult(
            student_id=student_id,
            quiz_id=quiz_id,
            score=score,
            total_questions=total_questions,
            percentage=percentage
        )
        db.session.add(result)
        db.session.commit()
        
        return result
