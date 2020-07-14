from app import db
from app.model.movies import Movie
from app.model.table_associations import UserMovies


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    movies = db.relationship("Movie", secondary=UserMovies, backref=db.backref("users"))
    orders = db.relationship("Order", backref="user")

    def user_dict(self, username=True):
        data = {
            "username": self.username,
            "user id": self.id,
            "watchlist": [m.movie_dict() for m in self.movies],
            "orders": [o.order_dict() for o in self.orders],
        }
        if not username:
            data = {
                self.username: {
                    "user id": self.id,
                    "watchlist": [
                        {m.title: m.movie_dict(title=False)} for m in self.movies
                    ],
                    "orders": [
                        {
                            "Order id:": o.id,
                            "Movie": self.get_movie_title_from_order(o.movie_id),
                            "Status": "Paid" if o.paid else "Not paid",
                        }
                        for o in self.orders
                    ],
                }
            }

        return data

    def get_movies(self):
        data = {"movies": [m.title for m in self.movies]}
        return data

    def get_movie_title_from_order(self, movie_id):
        for m in self.movies:
            if m.id == movie_id:
                return m.title

    def rent_movie(self, movie):
        self.movies.append(movie)

    def __repr__(self):
        return f"User: {self.username}"
