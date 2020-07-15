import re
from flask import request, jsonify, current_app
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


@bp.route("/users/", methods=["GET"])
@bp.route("/users", methods=["GET"])
@auth.login_required(role="administrator")
def list_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", current_app.config["PER_PAGE"], type=int)
    if request.args.get("user_id"):
        user = User.query.filter_by(id=request.args.get("user_id")).first()
        payload, status_code = (
            (user.user_dict(), 200) if user else ({"error": "User not found!"}, 404)
        )
    else:
        res = User.query.order_by(User.username.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        payload, status_code = (
            ({"Users": [user.user_dict() for user in res.items]}, 200)
            if res
            else ({"error": "No users found!"}, 404)
        )
    res = jsonify(payload)
    res.status_code = status_code
    return res


@bp.route("/users/<int:user_id>", methods=["PATCH"])
@auth.login_required
def update_username(user_id):
    user = User.query.filter_by(id=request.args.get(user_id)).first()
    if not user:
        if auth.current_user() == "admin":
            return not_found_response("User not found")
        return unauthorized_access()
    if not (auth.current_user() == "admin" or auth.username() == user.username):
        return unauthorized_access()
    username = request.args.get("username")
    if username:
        u = User.query.filter_by(username=username).first()
        if u:
            return already_exists_response(
                f"Username {u.username} is used by another user. Please user another username."
            )
        else:
            if not bool(re.search("[a-zA-Z]", username)):
                return bad_request_response("You cannot have an empty username.")
        user.username = username

    return successful_update()


@bp.route("/users/<int:user_id>/orders", methods=["GET"])
def list_user_orders(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        if auth.current_user() != "admin" and auth.username() != user.username:
            return unauthorized_access()
    if not user:
        return not_found_response(
            "The user_id provided does not match a user in the database."
        )
    payload = {
        "items": [
            {f"order id: {order.id}": order.ordered_movie.title, "Paid": order.paid}
            for order in user.orders
        ]
    }
    res = jsonify(payload)
    return res


@bp.route("/users/<int:user_id>/history", methods=["GET"])
@auth.login_required
def get_watched_history(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        if auth.current_user() != "admin" and auth.username() != user.username:
            return unauthorized_access()
    if not user:
        return not_found_response(
            message="The user_id provided does not match a user in the database."
        )
    payload = {"movies:": [movie.movie_dict() for movie in user.movies]}
    return jsonify(payload)
