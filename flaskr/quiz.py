import uuid, random
from flask import abort, request, jsonify
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

def get_quiz_questions():
    # check if the user has taken quiz for the day
    # if yes, return abort(403)
    try:
        questions = Question.query.limit(15).all()
        questions = [
            question.quiz_format() for
            question in questions
        ]
        # create a QuizSession instance to indicate the current user has taken quiz for the day
        # return quiz questions in appropriate format: options and question text only
        return jsonify(questions)
    except Exception:
        abort(422)

def mark_quiz():
    score = 0
    try:
        data = request.get_json()
        answers = data['answers']
        # if type(answers) != 'list' or not answers: 
        #     return abort(400)
    except IndexError:
        print('index error')
        abort(400, description='answers missing')
    except Exception: 
        print('unknown error')
        return abort(400)
    try:
        for answer in answers:
            user_answer = answer.get('user_answer', '')
            question_id = answer.get('question_id', '')
            question = Question.query.get(question_id)
            if question.answer and question.answer == user_answer:
                score += 1
    except Exception:
        return jsonify({
            'score': score
        })
        # also save user score
    # update user score in data base for the particular quiz
    return jsonify({
        'score': score
    })