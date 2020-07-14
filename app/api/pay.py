from flask import jsonify, request
from app import db
from app.api import bp
from app.model.orders import Order
from app.model.users import User
from app.api.errors import (
    not_found_response,
    already_exists_response,
    unauthorized_access,
    bad_request_response
)
from app.api.auth import auth


@bp.route("/pay", methods=["POST"])
@auth.login_required
def pay_title():
    order_id = request.args.get("order_id")
    amount = request.args.get("amount")
    if not order_id:
        return bad_request_response("You must the order_id param to pay an order.")
    if not amount:
        return bad_request_response("You must the amount param to pay an order.")
    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return not_found_response(
            "The order_id provided does not a match an order in the database."
        )
    u = User.query.filter_by(username=auth.username()).first()
    if not u or u.id != order.user_id:
        return unauthorized_access()
    if order.paid:
        return already_exists_response("The order is already paid.")
    if float(amount) < order.get_charge_per_order():
        return bad_request_response(f"The amount you have to pay is {order.get_charge_per_order()}")
    order.paid = True
    db.session.add(order)
    db.session.commit()
    payload = {"message": "Order successfully paid"}
    return jsonify(payload)
