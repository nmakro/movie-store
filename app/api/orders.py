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
        users = User.query.all()
        orders = Order.query.all()

        #payload = {"Orders": {order.id: [order.order_dict() for order in u.orders] for u in users}}
        payload = {"orders": [order.order_dict() for order in orders]}

    else:

        user = User.query.filter_by(username=auth.current_user()).first()
        if not user and not (
                auth.current_user() == "admin" or auth.username() == user.username
        ):
            return unauthorized_access()
        payload = {
            "orders": [
                {
                    "Order id:": o.id,
                    "Movie": user.get_movie_title_from_order(o.movie_id),
                    # "Date of order": o.date_purchased,
                    "Status": "Paid" if o.paid else "Not paid",
                }
                for o in user.orders
                if user.orders
            ]
        }
    res = jsonify(payload)
    return res
