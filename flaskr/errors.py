from flask import jsonify

def error400(message='bad request'):
    return jsonify({
        'message': message,
        'success': False,
        'status_code': 400
    }), 400

def error401(message='not unauthorized'):
    return jsonify({
        'message': message,
        'success': False,
        'status_code': 401
    }), 401

def error403(message='access denied'):
    return jsonify({
        'message': message,
        'success': False,
        'status_code': 403
    }), 403

def error405(message='method not allowed'):
    return jsonify({
        'message': message,
        'success': False,
        'status_code': 405
    }), 405

def error404(message='resource not found'):
    return jsonify({
        'message': message,
        'success': False,
        'status_code': 404
    }), 404

def error422(message='unable to process request'):
    return jsonify({
        'message': message,
        'success': False,
        'status': 422
    }), 422

def error_msg(message, code):
    return jsonify({
        'message': message,
        'success': False,
        'status_code': code
    }), code