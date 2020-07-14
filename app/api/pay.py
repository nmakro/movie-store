from flask import jsonify
from app import db
from app.api import bp
from app.model.orders import Order
from app.api.errors import not_found_response, already_exists_response
from app.api.auth import auth


@bp.route("/pay/<int:order_id>", methods=["POST"])
@auth.login_required
def pay_title(order_id):
    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return not_found_response(
            "The order_id provided does not a match an order in the database."
        )
    if auth.username() != order.user_id.username:
        return "Access Denied", 401
    if order.paid:
        return already_exists_response("The order is already paid.")
    order.paid = True
    db.session.add(order)
    db.session.commit()
    payload = {"message": "Order successfully paid"}
    return jsonify(payload)
