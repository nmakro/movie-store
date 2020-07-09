from flask import request
from app.api import bp


@bp.route("/categories/<int:id>", methods=["GET"])
def get_category(id):
    pass


@bp.route("/categories", methods=["GET"])
def get_categories():
    pass


@bp.route("/categories/<int:id>/movies>", methods=["GET"])
def get_category_movies():
    pass


@bp.route("/categories/all/movies", methods=["GET"])
def get_all_categorized_movies():
    pass
