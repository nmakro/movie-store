import re
from flask import request, jsonify
from app.api import bp
from app.api.errors import (
    not_found_response,
    unauthorized_acess,
    already_exists_response,
    bad_request_response,
    successful_update,
)
from app.model.users import User
from app.api.auth import auth


@bp.route("/users/", methods=["GET"])
@bp.route("/users", methods=["GET"])
@auth.login_required(role="administrator")
def get_users():
    if request.args.get("user_id"):
        user = User.query.filter_by(id=request.args.get("user_id")).first()
        payload, status_code = (
            (user.user_dict(), 200) if user else ({"error": "User not found!"}, 404)
        )
    else:
        res = User.query.order_by(User.username.desc()).paginate(1, 20, False).items
        payload, status_code = (
            ({"Users": [user.user_dict(username=False) for user in res]}, 200)
            if res
            else ({"error": "User not found!"}, 404)
        )
    res = jsonify(payload)
    res.status_code = status_code
    return res


@bp.route("/users/<int:user_id>", methods=["PATCH"])
@auth.login_required
def update_username(user_id):
    user = User.query.filter_by(id=request.args.get(user_id)).first()
    if not user:
        return not_found_response("User not found!")
    else:
        if not (auth.current_user() == "admin" or auth.username() == user.username):
            return unauthorized_acess()
        for param in request.args.keys():
            if param == "username":
                if user.username == request.args.get(param):
                    res = jsonify({})
                    res.status_code = 201
                    return res
                else:
                    u = User.query.filter_by(username=request.args.get(param))
                    if u:
                        return already_exists_response(
                            f"Username {u.username} is used by another user. Please user another username."
                        )
                    elif not bool(re.search("[a-zA-Z]", request.args.get(param))):
                        return bad_request_response(
                            "You cannot have an empty username."
                        )
                    else:
                        user.username = request.args.get(param)
                        break

    return successful_update()


@bp.route("/users/<int:user_id>", methods=["PUT"])
@auth.login_required
def update_user(user_id):
    user = User.query.filter_by(id=request.args.get(user_id)).first()
    if not user:
        return not_found_response("User not found!")
    else:
        if not (auth.current_user() == "admin" or auth.username() == user.username):
            return unauthorized_acess()
        for param in request.args.keys():
            if param == "id":
                continue
            else:
                if param == "username":
                    if not bool(re.search("[a-zA-Z]", request.args.get(param))):
                        return bad_request_response(
                            "You cannot have an empty username."
                        )
                    u = User.query.filter_by(username=request.args.get(param))
                    if u:
                        return already_exists_response(
                            f"Username {u.username} is used by another user. Please user another username."
                        )
                    user.username = request.args.get(param)
                if param == "movie":
                    if request.args.get(param) in user.movies:
                        continue
                    elif request.args.get(param) == "":
                        for order in user.orders:
                            if not order.paid and order.ordered_movie in user.movies:
                                return bad_request_response(
                                    "In order to delete movies from your watchlist, you must first pay all pending subscriptions."
                                )
                        user.movies = []
                    else:
                        continue
    res = jsonify({})
    res.status_code = 201
    return res


@bp.route("/users/<int:user_id>/orders", methods=["GET"])
def user_orders(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        if auth.current_user() != "admin" and auth.username() != user.username:
            return unauthorized_acess()
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
def get_watched_history(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        if auth.current_user() != "admin" and auth.username() != user.username:
            return unauthorized_acess()
    if not user:
        return not_found_response(
            message="The user_id provided does not match a user in the database."
        )
    payload = {"Movies watched:": [movie.movie_dict() for movie in user.movies]}
    return jsonify(payload)
