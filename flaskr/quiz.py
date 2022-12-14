import uuid, random, json, pytz
from datetime import datetime
from flask import abort, request, jsonify
from sqlalchemy import desc, and_
from .models import Question, QuizSession, Leaderboard
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

    # if day in no_quiz_days:
    #     print('there is no quiz today')
    #     abort(403, description='no quiz today')

    quiz_session =  QuizSession.query.filter(
        QuizSession.user_id == current_user.id
    ).order_by(desc(QuizSession.date_created)).first()

    if quiz_session:
        session_date = quiz_session.date_created.date()
        if session_date == today.date():
            abort(403, description='you have already taken quiz for the day')
    
    try:
        questions = Question.query.limit(15).all()
        if not questions:
            abort(403, description='no quiz today')
        questions = [
            question.quiz_format() for
            question in questions
        ]
        quiz_session = QuizSession(
            public_id = str(uuid.uuid4()).replace('-', ''),
            user_id = current_user.id,
            questions = json.dumps(questions),
            date_created = today,
            last_updated = today,
            completed = False
        )
        quiz_session.insert()
        return jsonify({
            'questions': questions,
            'quiz_id': quiz_session.public_id
        })
    except Exception:
        abort(422)

def mark_quiz(current_user):

    try:
        request_data = request.get_json()
        quiz_id = request_data['quiz_id']
        answers = request_data['answers']
    except Exception:
        abort(400, description='missing data')

    quiz_session = QuizSession.query.filter(
        and_(QuizSession.public_id == quiz_id, QuizSession.user_id==current_user.id)
    ).first()

    if not quiz_session:
        abort(403, description='you have not taken quiz')

    if quiz_session.completed == True:
        abort(403, description='quiz already graded')

    score = 0
    cp = 0
    cap = 0
   
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
        quiz_session.last_updated = today
        quiz_session.completed = True
        quiz_session.update()
        current_user.cp += cp
        current_user.cap += cap
        current_user.update()

        leaderboard_profile = current_user.leaderboard_profile
        if not leaderboard_profile:
            leaderboard_profile = Leaderboard(
                public_id = str(uuid.uuid4()).replace('-', ''),
                user_id = current_user.id,
                cap = cap,
                cp = cap,
                points = score,
                date_created = today,
                last_updated = today
            )
            leaderboard_profile.insert()
        else:
            leaderboard_profile.cap += cap
            leaderboard_profile.cp += cp
            leaderboard_profile.points += score
            leaderboard_profile.last_update = today
            leaderboard_profile.update()

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

def user_quiz_sessions(current_user):
    sessions = []

    quizzes = QuizSession.query.filter(
        QuizSession.user_id==current_user.id
    ).order_by(desc(QuizSession.date_created)).all()

    if quizzes:
        sessions = [
            quiz.format() for quiz in quizzes
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
