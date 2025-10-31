from flask import jsonify


def bad_request_response(message=None):
    payload = {"error": 400}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = 400
    return response


def already_exists_response(message=None):
    payload = {"error": 409}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = 409
    return response


def not_found_response(message=None):
    payload = {"error": 404}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = 404
    return response


def unauthorized_access():
    payload = {"error": 401, "message": "Access denied:"}
    response = jsonify(payload)
    response.status_code = 401
    return response


def successful_update(message=None):
    payload = {}
    if message:
        payload["message"] = message
    res = jsonify(payload)
    res.status_code = 204
    return res
