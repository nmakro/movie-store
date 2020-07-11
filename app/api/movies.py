from flask import jsonify
from app.api import bp
from app.model.movies import Movie


@bp.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie_from_id(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    payload, status_code = (movie.movie_dict, 200) if movie else ({"error": "Movie not found"}, 404)
    res = jsonify(payload)
    res.status_code = status_code
    return res


@bp.route("/movies/<string:title>", methods=["GET"])
def get_movie_from_title(title):
    movie = Movie.query.filter_by(title=title).first()
    payload, status_code = (movie.movie_dict(), 200) if movie else ({"error": "Movie not found"}, 404)
    res = jsonify(payload)
    res.status_code = status_code
    return res


@bp.route("/movies", methods=["GET"])
@bp.route("/movies/", methods=["GET"])
def get_movies():
    res = Movie.query.order_by(Movie.id.desc()).paginate(1, 20, False).items
    data = {"items": {"movies": [{movie.title: movie.movie_dict()} for movie in res]}}
    return jsonify(data)
