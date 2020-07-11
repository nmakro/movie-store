from app import db


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    director = db.Column(db.String(64))
    year = db.Column(db.String(4))
    title = db.Column(db.String(64))

    def __repr__(self):
        return f"{self.title}"
