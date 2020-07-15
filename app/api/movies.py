from flask import jsonify, request, url_for, current_app
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


@bp.route("/movies/", methods=["GET"])
def list_movies():
    genre = request.args.get("genre")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", current_app.config["PER_PAGE"], type=int)

    res = Movie.query.order_by(Movie.title.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    next_url = (
        url_for("api.list_movies", page=res.next_num, genre=genre)
        if res.has_next
        else None
    )
    prev_url = (
        url_for("api.list_movies", page=res.prev_num, genre=genre)
        if res.has_prev
        else None
    )
    data = {
        "_meta": {"next": next_url, "prev": prev_url},
        "movies": [movie.movie_dict() for movie in res.items],
    }
    return jsonify(data)


@bp.route("/movies/search", methods=["GET"])
def search_movies():
    genre = request.args.get("genre")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", current_app.config["PER_PAGE"], type=int)
    if not genre:
        return bad_request_response(
            "You must specify a category using the genre parameter to search for a movie"
        )
    g = Category.query.filter_by(genre=genre).first()
    if not g:
        return bad_request_response(f"Genre {genre} not found!")
    titles = []
    for m in g.movies:
        titles.append(m.title)
    res = Movie.query.filter(Movie.title.in_(titles)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    next_url = (
        url_for("api.list_movies", page=res.next_num, genre=genre)
        if res.has_next
        else None
    )
    prev_url = (
        url_for("api.list_movies", page=res.prev_num, genre=genre)
        if res.has_prev
        else None
    )
    data = {
        "_meta": {"next": next_url, "prev": prev_url},
        "movies": [movie.movie_dict() for movie in res.items],
    }
    return jsonify(data)


@bp.route("/movies", methods=["PATCH"])
@auth.login_required(role="administrator")
def update_movie():
    movie_id = request.args.get("movie_id")
    if not movie_id:
        return bad_request_response(
            "You must use the movie_id param in order to update a movie."
        )
    m = Movie.query.filter_by(id=movie_id).first()
    if m is None:
        return not_found_response(
            "The movie_id provided does not a match a movie in the database."
        )
    for param in request.args.keys():
        if param not in ["id", "orders"] and hasattr(m, param):
            if param == "genre":
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
    if title is None or director is None:
        return bad_request_response(
            "You must the specify the title and director params in order to create a movie"
        )
    m = Movie.query.filter_by(title=title, director=director).first()
    if m:
        return already_exists_response("The movie provided is already in the database.")
    new_movie = Movie()
    for param in request.args.keys():
        if hasattr(new_movie, param):
            setattr(new_movie, param, str(request.args.get(param)))
        elif param == "genre":
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
