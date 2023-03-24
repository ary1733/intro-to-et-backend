from flask import Blueprint
user_blueprint = Blueprint('user',__name__,url_prefix="/api/v1/user")

# This import might seem unconventional, however is required to register your
# routes, which are created.
from src.user import controller