from flask import jsonify
from app.api import bp
from app.model.users import User
from app.model.orders import Order
from app.api.errors import unauthorized_access
from app.api.auth import auth


@bp.route("/orders", methods=["GET"])
@auth.login_required
def list_orders():
    if auth.current_user() == "admin":
        orders = Order.query.all()
        payload = {"orders": [order.order_dict() for order in orders]}
    else:
        user = User.query.filter_by(username=auth.current_user()).first()
        if not user and not (
            auth.current_user() == "admin" or auth.username() == user.username
        ):
            return unauthorized_access()
        payload = {
            "orders": [o.order_dict() for o in user.orders]
        }
    res = jsonify(payload)
    return res
