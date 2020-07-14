from flask import jsonify, request, url_for
from app.api import bp
from app import db
from app.api.errors import (
    bad_request_response,
    not_found_response,
    already_exists_response,
    successful_update,
)
from app.model.movies import Movie
from app.api.categories import Category
from app.api.auth import auth


@bp.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie_from_id(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    payload, status_code = (
        (movie.movie_dict(), 200) if movie else ({"error": "Movie not found"}, 404)
    )
    res = jsonify(payload)
    res.status_code = status_code
    return res


@bp.route("/movies/search/", methods=["GET"])
def get_movie_from_title():
    title = request.args.get("title")
    if not title:
        return bad_request_response(
            "You must specify the title param in order to search a movie"
        )
    movies = Movie.query.filter_by(title=title).all()
    payload = {"movies": [m.dict for m in movies]}
    res = jsonify(payload)
    return res


@bp.route("/movies/", methods=["GET"])
@bp.route("/movies", methods=["GET"])
def list_movies():
    res = Movie.query.order_by(Movie.id.desc()).paginate(1, 20, False).items
    data = {"items": {"movies": [movie.movie_dict() for movie in res]}}
    return jsonify(data)


@bp.route("/movies/<int:movie_id>", methods=["PATCH"])
@auth.login_required(role=["administrator"])
def update_movie(movie_id):
    m = Movie.query.filter_by(id=movie_id).first()
    if m is None:
        return not_found_response(
            "The movie_id provided does not a match a movie in the database."
        )
    for param in request.args.keys():
        if param not in ["id", "orders"] and hasattr(m, param):
            if param == "category":
                c = Category.query.filter_by(genre=request.args.get(param)).first()
                if not c:
                    return not_found_response(
                        "There is no such category in the database."
                    )
                else:
                    m.category.append(c)
            else:
                setattr(m, param, str(request.args.get(param)))

    db.session.add(m)
    db.session.commit()
    res = jsonify({})
    res.status_code = 204
    res.headers["Location"] = url_for("api.get_movie_from_id", movie_id=m.id)

    return res


@bp.route("/movies", methods=["POST"])
@auth.login_required(role="administrator")
def create_movie():
    title = request.args.get("title")
    director = request.args.get("director")
    if title is None and director is None:
        return bad_request_response(
            "You must the specify the title and director params in order to create a movie"
        )
    m = Movie.query.filter_by(title=title, director=director).first()
    if m:
        return already_exists_response("The movie provided is already in the database.")
    req_json = request.args.keys()
    new_movie = Movie()
    for param in req_json:
        if hasattr(new_movie, param):
            setattr(new_movie, param, str(request.args.get(param)))
        else:
            c = Category.query.filter_by(genre=request.args.get(param)).first()
            if not c:
                return not_found_response("There is no such category in the database.")
            else:
                m.category.append(c)

    db.session.add(new_movie)
    db.session.commit()
    res = jsonify({})
    res.status_code = 201
    res.headers["Location"] = url_for("api.get_movie_from_id", movie_id=new_movie.id)

    return res


@bp.route("/movies/<int:movie_id>", methods=["DELETE"])
@auth.login_required(role="administrator")
def delete_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return not_found_response("Movie not found.")
    db.session.delete(movie)
    db.session.commit()

    return successful_update()
