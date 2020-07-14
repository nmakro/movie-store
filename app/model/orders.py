from datetime import datetime
from app import db
from app.model.movies import Movie


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
            "movie": self.movie_id
        }
        return data

    def __repr__(self):
        return f"Order: {self.id}"
