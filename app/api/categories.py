from flask import jsonify, request
from app import db
from app.api import bp
from app.api.errors import bad_request_response, already_exists_response, not_found_response, successful_update
from app.model.categories import Category
from app.api.auth import auth


@bp.route("/categories/", methods=["GET"])
@bp.route("/categories", methods=["GET"])
def get_categories():
    if len(request.args) > 0:
        genre = request.args.get("genre")
        if genre:
            if genre == "all":
                items = Category.query.order_by(Category.genre.desc()).paginate(1, 20, False).items
                data, status_code = ({"items": [c.category_dict() for c in items]}, 200) if items else ({"error:": "Category not found!"}, 404)
            else:
                c = Category.query.filter_by(genre=genre).first()
                data, status_code = ({"category": c.genre, "movies": [m.movie_dict(genre=False) for m in c.movies]}, 200) if c is not None else ({"error:": "Category not found!"}, 404)
        else:
            data, status_code = ({"error": "Unknown query param"}, 400)
    else:
        items = Category.query.order_by(Category.genre.desc()).paginate(1, 20, False).items
        data, status_code = ({"items": [c.genre for c in items]}, 200) if items else ({"error:": "No categories found"}, 404)
    res = jsonify(data)
    res.status_code = status_code
    return res


@bp.route("/categories", methods=["POST"])
@auth.login_required(role="administrator")
def add_category():
    genre = request.args.get("genre")
    if genre is None:
        return bad_request_response("You must specify the genre param in order to create a new category.")
    if Category.query.filter_by(genre=genre).first() is not None:
        return already_exists_response("The category you specified already exists.")
    c = Category(genre=genre)
    db.session.add(c)
    db.session.commit()
    res = jsonify({})
    res.status_code = 201
    return res


@bp.route("/categories", methods=["DELETE"])
@auth.login_required(role="administrator")
def delete_category():
    category_id = request.args.get("id")
    genre = request.args.get("genre")
    if not (genre or category_id):
        return bad_request_response("You must specify the genre or id param in order to delete a category.")
    if genre:
        c = Category.query.filter_by(genre=genre).first()
        if c is None:
            return not_found_response("The category you specified does not exist.")
    else:
        c = Category.query.filter_by(genre=genre).first()
        if c is None:
            return not_found_response("The category you specified does not exist.")
    db.session.delete(c)
    db.session.commit()

    return successful_update()
