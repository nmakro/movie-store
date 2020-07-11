from app import db
from app.model.table_associations import UserMovies


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    movies = db.relationship("Movie", secondary=UserMovies, backref=db.backref("movies"))

    def user_dict(self):
        data = {
            "username": self.username,
            "movies": [m.title for m in self.movies]
        }
        return data

    def get_movies(self):
        data = {
            "movies": [m.title for m in self.movies]
        }
        return data

    def __repr__(self):
        return f"User: {self.username}"
