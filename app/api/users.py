from flask import request, jsonify
from app.api import bp
from app.model.users import User


@bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    payload, status_code = (user.user_dict(), 200) if user else ({"error": "User not found"}, 404)
    res = jsonify(payload)
    res.status_code = status_code
    return res


@bp.route("/users/<string:username>", methods=["GET"])
def get_user_by_name(username):
    user = User.query.filter_by(username=username).first()
    payload, status_code = (user.user_dict(), 200) if user else ({"error": "User not found"}, 404)
    res = jsonify(payload)
    res.status_code = status_code
    return res


@bp.route("/users/", methods=["GET"])
@bp.route("/users", methods=["GET"])
def get_users():
    if request.args.get("username"):
        user = User.query.filter_by(username=request.args.get("username")).first()
        payload, status_code = (user.user_dict(), 200) if user else ({"error": "User not found"}, 404)
    else:
        res = User.query.order_by(User.username.desc()).paginate(1, 20, False).items
        payload, status_code = ({"items": [user.user_dict() for user in res]}, 200) if res else ({"error": "No users found!"}, 404)
    res = jsonify(payload)
    res.status_code = status_code
    return res


@bp.route("/users/<string:username>/history", methods=["GET"])
def user_movies(user_id):
    pass

