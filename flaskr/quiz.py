import uuid, random
from flask import request, jsonify
from .models import Question
from .errors import error400, error404, error422

def quiz_question():
    try:
        data = request.get_json()
        prev_id = data.get('prev_id', [])
    except Exception: return error400(message='all is well')
    try :
        questions = Question.query.filter(Question.id.not_in(prev_id))
        questions = [
            question.format() for
            question in questions
        ]
        quiz_question = random.choice(questions)
    except IndexError:
        return error404()
    return jsonify(quiz_question)

def mark_quiz():
    pass
