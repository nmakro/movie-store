from flask import request, jsonify
from app.api import bp
from app.model.users import User


@bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify(User.query.get_or_404(user_id).user_dict())


@bp.route("/users", methods=["GET"])
def get_users():
    res = User.query.order_by(User.id.desc()).paginate(1, 20, False).items
    data = {"items": [user.user_dict() for user in res]}
    return jsonify(data)


@bp.route("/users/<int:user_id>/movies", methods=["GET"])
def user_movies(user_id):
    return jsonify(User.query.get_or_404(user_id).get_movies())

