from flask import Blueprint

bp = Blueprint("api", __name__)

from . import movies, users, errors, categories, rent, pay, home, orders
