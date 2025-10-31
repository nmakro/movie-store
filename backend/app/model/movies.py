from app import db
from app.model.table_associations import MovieCategories


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    director = db.Column(db.String(64))
    year = db.Column(db.String(4))
    title = db.Column(db.String(64))
    category = db.relationship("Category", secondary=MovieCategories)
    orders = db.relationship("Order", backref="ordered_movie")

    def movie_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "director": self.director,
            "year": self.year,
            "genre": [c.genre for c in self.category],
        }

        return data

    def __repr__(self):
        return f"{self.title}"
