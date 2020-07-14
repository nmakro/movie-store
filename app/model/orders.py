from datetime import datetime
from app import db


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date_purchased = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    paid = db.Column(db.Boolean, index=True, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"))

    def order_dict(self):
        data = {
            "order id": self.id,
            "order date": self.date_purchased,
            "status": "Paid" if self.paid else "Not paid",
            "user id": self.user_id,
            "movie": self.movie_id,
            "charge price": self.get_charge_per_order(),
        }
        return data

    def get_charge_per_order(self):
        now = datetime.now()
        days_passed = (now - self.date_purchased).days
        charge = 1
        if days_passed > 3:
            charge += charge + (days_passed - 3) * 0.5
        return charge

    def __repr__(self):
        return f"Order: {self.id}"
