from flask import request, jsonify
from app.api import bp
from app import db
from app.model.movies import Movie
from app.model.users import User


@bp.route("/rent/<string:username>", methods=["POST"])
def rent_title(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        payload = {"error": "User not found"}
        res = jsonify(payload)
        res.status_code = 400
        return res
    movie_id = request.args.get("movie_id")
    movie_name = request.args.get("movie_name")
    if movie_id is None and movie_name is None:
        payload, status_code = {"error": "Please provide either the movie_id or movie_name for the movie you want to rent!"}, 404
        res = jsonify(payload)
        res.status_code = 400
        return res
    elif movie_name is not None:
        movie = Movie.query.filter_by(title=movie_name).first()
        if not movie:
            payload = {"error": "Movie not found"}
            res = jsonify(payload)
            res.status_code = 404
            return res
        user.rent_movie(movie)
        db.session.add(user)
        db.session.commit()
        res = jsonify({})
        res.status_code = 201
        return res



