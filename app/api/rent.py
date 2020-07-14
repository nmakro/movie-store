from flask import jsonify
from app.api import bp
from app import db
from app.model.movies import Movie
from app.model.users import User
from app.api.errors import not_found_response, already_exists_response
from app.model.orders import Order
from app.api.auth import auth


@bp.route("/rent/<int:movie_id>", methods=["POST"])
@auth.login_required()
def rent_title(movie_id):
    user = User.query.filter_by(username=auth.username()).first()
    if not user and auth.username() != user.username:
        return "Access Denied", 401
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return not_found_response(
            "The movie_id provided does not match a movie in the database."
        )
    order = Order.query.filter_by(movie_id=movie_id, user_id=user.id).first()
    if order:
        return already_exists_response("You have already purchased this movie.")
    new_order = Order(movie_id=movie_id, user_id=user.id)
    user.rent_movie(movie)
    db.session.add(new_order)
    db.session.commit()
    res = jsonify({})
    res.status_code = 201
    return res
