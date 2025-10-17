from flask import Blueprint

home_bp = Blueprint("home_bp", __name__)


@home_bp.get("/")
def home():
    return "<h1> Welcome to Book Search </h1>"