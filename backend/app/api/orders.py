from flask import jsonify, request, current_app, url_for
from app.api import bp
from app.model.users import User
from app.model.orders import Order
from app.api.errors import unauthorized_access
from app.api.auth import auth


@bp.route("/orders", methods=["GET"])
@auth.login_required
def list_orders():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", current_app.config["PER_PAGE"], type=int)
    if auth.current_user() == "admin":
        orders = Order.query.order_by(Order.id.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    else:
        user = User.query.filter_by(username=auth.current_user()).first()
        if not user or not auth.username() == user.username:
            return unauthorized_access()
        orders = Order.query.filter_by(user_id=user.id).paginate(
            page=page, per_page=per_page, error_out=False
        )

    next_url = (
        url_for("api.list_orders", page=orders.next_num) if orders.has_next else None
    )
    prev_url = (
        url_for("api.list_orders", page=orders.prev_num) if orders.has_prev else None
    )
    payload = {
        "_meta": {"next": next_url, "prev": prev_url},
        "orders": [order.order_dict() for order in orders.items],
    }

    res = jsonify(payload)
    return res
