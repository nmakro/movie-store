from flask import jsonify
from app.api import bp
from app.model.movies import Movie


@bp.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    return jsonify(Movie.query.get_or_404(movie_id).movie_dict())


@bp.route("/movies/", methods=["GET"])
def get_movies():
    res = Movie.query.order_by(Movie.id.desc()).paginate(1, 20, False).items
    data = {"items": [movie.movie_dict() for movie in res]}
    return jsonify(data)
