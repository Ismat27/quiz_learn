import  uuid
from flask import jsonify,request, abort
from .models import Question
from .errors import error400, error404, error422

def get_question(id):
    data = Question.query.get(id)
    if not data: return abort(404, description='resource not found')
    return data

def create_question():
    data = request.get_json()
    if not data: return error400(message='data missing')
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
        return error400(message='key error')

    for key in data.keys():
        if not data[key] and key not in ['cp_wrong', 'cap_wrong']:
            return error400(message='empty data')
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
        question.insert()
        return jsonify({
            'success': True
        })
    except Exception as error:
        return error422()

def all_questions():
    questions = Question.query.all()
    if questions:
        questions = [
            question.format() for
            question in questions
        ]
    return jsonify(questions)

def question_data(id):
    question = get_question(id)
    return jsonify(question.format())

def edit_question(id):
    question = get_question(id)
    data = request.get_json()
    if not data: return error400(message='data missing')
    for key in data.keys():
        if not data[key] and key not in ['cp_wrong', 'cap_wrong']:
            return error400(message='empty data')
    try:
        question.text = data.get('text', question.text)
        question.option_a = data.get('option_a', question.option_a)
        question.option_b = data.get('option_b',question.option_b)
        question.option_c = data.get('option_c', question.option_c)
        question.option_d = data.get('option_d', question.option_d)
        question.answer = data.get('answer', question.answer)
        question.cp_wrong = data.get('cp_wrong', question.cp_wrong)
        question.cp_right = data.get('cp_right', question.cp_right)
        question.cap_wrong = data.get('cap_wrong', question.cap_wrong)
        question.cap_right = data.get('cap_right', question.cap_right)
        question.update()
    except Exception as error:
        return error400(message='key error')
    return jsonify(question.format())
    
def delete_question(id):
    question = get_question(id)
    question.delete()
    return jsonify({'id': id})

