from app.api import bp


@bp.route("/rent/<int:title-id>", methods=["POST"])
def rent_title():
    pass

