from app import db
from app.model.table_associations import MovieCategories


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    director = db.Column(db.String(64))
    year = db.Column(db.String(4))
    title = db.Column(db.String(64))
    categories = db.relationship("Category", secondary=MovieCategories, backref=db.backref("movie_categories"))

    def movie_dict(self):
        data = {
                "title": self.title,
                "director": self.director,
                "year": self.year,
                "categories": [c.genre for c in self.categories]
            }

        return data

    def __repr__(self):
        return f"{self.title}"
