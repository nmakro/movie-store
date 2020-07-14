from datetime import datetime
from app import db


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date_purchased = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    paid = db.Column(db.Boolean, index=True, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))

    def __repr__(self):
        return f"Order: {self.id}"
