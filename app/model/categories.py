from app import db
from app.model.table_associations import MovieCategories


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String, index=True, unique=True)
    movies = db.relationship("Movie", secondary=MovieCategories)

    def category_dict(self):
        data = {"genre": self.genre, "movies": [m.title for m in self.movies]}

        return data

    def __repr__(self):
        return f"{self.genre}"
