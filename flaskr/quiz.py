import uuid, random, json, pytz
from datetime import datetime
from flask import abort, request, jsonify
from sqlalchemy import desc
from .models import Question, QuizSession
from .errors import error400, error404, error422

my_timezone = pytz.timezone('Africa/Lagos')
today = datetime.now(my_timezone)
no_quiz_days = ['saturday', 'sunday']
day = today.strftime('%A').lower()

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

def get_quiz_questions(current_user):

    if day in no_quiz_days:
        print('there is no quiz today')
        abort(403, description='no quiz today')

    quiz_session =  QuizSession.query.filter(
        QuizSession.user_id == current_user.id
    ).order_by(desc(QuizSession.date_created)).first()

    if quiz_session:
        session_date = quiz_session.date_created.date()
        print(session_date == today.date())
        abort(403, description='you have already taken quiz for the day')
    
    try:
        questions = Question.query.limit(15).all()
        questions = [
            question.quiz_format() for
            question in questions
        ]
        if not questions:
            abort(403, description='no quiz today')
        quiz_session = QuizSession(
            public_id = str(uuid.uuid4()).replace('-', ''),
            user_id = current_user.id,
            questions = json.dumps(questions),
            completed = False
        )
        quiz_session.insert()
        return jsonify(questions)
    except Exception:
        abort(422)

def mark_quiz(current_user):

    quiz_session =  QuizSession.query.filter(
        QuizSession.user_id == current_user.id
    ).order_by(desc(QuizSession.date_created)).first()

    if not quiz_session:
        abort(403, description='you have not taken quiz')

    if quiz_session.completed == True:
        abort(403, description='quiz already graded')


    score = 0
    cp = 0
    cap = 0
    try:
        data = request.get_json()
        answers = data['answers']
    except IndexError:
        abort(400, description='answers missing')
    except Exception: 
        return abort(400)
    try:
        for answer in answers:
            user_answer = answer.get('user_answer', '')
            question_id = answer.get('question_id', '')
            question = Question.query.get(question_id)
            if question:
                if question.answer == user_answer:
                    score += 1
                    cp += question.cp_right
                    cap += question.cap_right
                else:
                    cp += question.cp_wrong
                    cap += question.cap_wrong
        quiz_session.score = score
        quiz_session.completed = True
        quiz_session.update()
        current_user.cp += cp
        current_user.cap += cap
        current_user.update()
        return jsonify({
            'score': score,
            'challenge_points': cp,
            'course_access_points': cap
        })

    except Exception:
        return jsonify({
            'score': score
        })


def quiz_sessions():
    sessions = QuizSession.query.order_by(desc(QuizSession.date_created)).all()
    sessions = [
        session.format() for
        session in sessions
    ]
    return jsonify(sessions)

def delete_quiz_session(session_id):
    session = QuizSession.query.get(session_id)
    if not session:
        abort(404, description='resource not found')
    try:
        session.delete()
        return jsonify({
            'success': True,
            'message': 'deleted successfully'
        })
    except Exception:
        abort(422)
