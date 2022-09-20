import uuid, random
from flask import request, jsonify
from .models import Question
from .errors import error400, error422

def create_question():
    data = request.get_json()
    if not data: return error400()
    try:
        text = data['text']
        option_a = data['option_a']
        option_b = data['option_b']
        option_c = data['option_c']
        option_d = data['option_d']
        answer = data['answer']
        cp_wrong = data['cp_wrong']
        cp_right = data['cp_right']
        cap_wrong = data['cap_wrong']
        cap_right = data['cap_right']
    except KeyError:
        return error400()

    for key in data.keys():
        if not data[key]:
            return error400()
    try:
        question = Question(
            public_id = str(uuid.uuid4()).replace('-', ''),
            text=text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            answer=answer,
            cp_right=cp_right,
            cp_wrong=cp_wrong,
            cap_right=cap_right,
            cap_wrong=cap_wrong,
        )
        # question.insert()
        return jsonify({
            'success': True
        })
    except Exception as error:
        return error422()

def quiz_question():
    prev_id = request.get_json().get('prev_id', [])
    questions = Question.query.filter(Question.id.not_in(prev_id))
    questions = [
        question.format() for
        question in questions
    ]
    quiz_question = random.choice(questions)
    return jsonify(quiz_question)
