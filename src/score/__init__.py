from flask import Blueprint
post_blueprint = Blueprint('post',__name__,url_prefix="/api/v1/post")

# This import might seem unconventional, however is required to register your
# routes, which are created.
from src.score import controller