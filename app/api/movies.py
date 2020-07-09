from app.api import bp


@bp.route("/movies/<int:id>", methods=["GET"])
def get_movie(id):
    pass


@bp.route("/movies/", methods=["GET"])
def get_movies():
    pass
