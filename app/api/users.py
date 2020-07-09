from flask import request
from app.api import bp


@bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    pass


@bp.route("/users/", methods=["GET"])
def get_users(id):
    pass


@bp.route("/users/<int:id>/movies", methods=["GET"])
def user_movies(id):
    pass


@bp.route("/users/all/movies", methods=["GET"])
def get_all_movies_rent():
    pass


@bp.route("user/<int:id>/history", methods=["GET"])
def get_user_history():
    pass
