from flask import jsonify, request, url_for
from app import db
from moviestore import app
from app.api import bp
from app.api.errors import bad_request_response, already_exists_response, not_found_response, successful_update
from app.model.categories import Category
from app.api.auth import auth


@bp.route("/categories/", methods=["GET"])
def list_categories():
    genre = request.args.get("genre")
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', app.config['PER_PAGE'], type=int)
    if genre:
        if genre == "all":
            categories = Category.query.order_by(Category.genre.desc()).paginate(page, per_page, False)
        else:
            categories = Category.query.filter_by(genre=genre).paginate(page, per_page, False)
        next_url = url_for('api.list_categories', page=categories.next_num, genre=genre) \
            if categories.has_next else None
        prev_url = url_for('api.list_categories', page=categories.prev_num, genre=genre) \
            if categories.has_prev else None
        data, status_code = ({"_meta": {"next": next_url, "prev": prev_url}, "categories": [c.category_dict() for c in categories.items]}, 200) \
            if categories.items else ({"error:": "Category not found!"}, 404)

    else:
        items = Category.query.order_by(Category.genre.desc())
        data, status_code = ({"categories": [c.genre for c in items]}, 200) if items else ({"error:": "No categories found"}, 404)
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
    if genre == "all":
        return bad_request_response("You cannot add 'all' as a genre.")
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
