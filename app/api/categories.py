from flask import jsonify, request
from app.api import bp
from app.model.categories import Category


@bp.route("/categories/", methods=["GET"])
@bp.route("/categories", methods=["GET"])
def get_categories():
    if len(request.args) > 0:
        genre = request.args.get("genre")
        if genre:
            if genre == "all":
                items = Category.query.order_by(Category.genre.desc()).paginate(1, 20, False).items
                data, status_code = ({"items": [c.category_dict() for c in items]}, 200) if items else ({"error:": "No categories found"}, 404)
            else:
                c = Category.query.filter_by(genre=genre).first()
                data, status_code = ({"category": c.genre, "movies": [m.title for m in c.movies]}, 200) if c is not None else ({"movies": []}, 404)
        else:
            data, status_code = ({"error": "Unknown query param"}, 400)
    else:
        items = Category.query.order_by(Category.genre.desc()).paginate(1, 20, False).items
        data, status_code = ({"items": [c.genre for c in items]}, 200) if items else ({"error:": "No categories found"}, 404)
    res = jsonify(data)
    res.status_code = status_code
    return res
