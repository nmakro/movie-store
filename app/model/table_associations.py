from app import db

UserMovies = db.Table("user_movies",
                      db.Column("id", db.Integer, primary_key=True),
                      db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="cascade")),
                      db.Column("movie_id", db.Integer, db.ForeignKey("movies.id", ondelete="cascade"))
                      )
