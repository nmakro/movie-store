from app import create_app
from app import db
from app.model.categories import Category
from app.model.movies import Movie
from app.model.users import User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Movie': Movie, 'Category': Category}


if __name__ == "__main__":
    app.run()
