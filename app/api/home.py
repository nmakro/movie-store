from flask import request, jsonify
from app.api import bp
from app.api.errors import (
    not_found_response,
    unauthorized_access,
    already_exists_response,
    bad_request_response,
    successful_update,
)
from app.model.users import User
from app.api.auth import auth


@bp.route("/home/")
@bp.route("/home")
@auth.login_required
def get_home_page():
    if auth.username() == "admin":
        payload = {"message": "You are admin"}
        return jsonify(payload)
    user = User.query.filter_by(username=auth.current_user()).first()
    if not auth.username() == user.username:
        return unauthorized_access()
    payload, status_code = user.user_dict(), 200
    res = jsonify(payload)
    res.status_code = status_code
    return res
