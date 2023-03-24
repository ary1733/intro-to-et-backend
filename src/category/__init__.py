from flask import Blueprint
category_blueprint = Blueprint('category',__name__,url_prefix="/api/v1/category")

# This import might seem unconventional, however is required to register your
# routes, which are created.
from src.category import controller