from app import db

UserMovies = db.Table(
    "user_movies",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="cascade")),
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id", ondelete="cascade")),
)

MovieCategories = db.Table(
    "movie_categories",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "category_id", db.Integer, db.ForeignKey("categories.id", ondelete="cascade")
    ),
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id", ondelete="cascade")),
)
