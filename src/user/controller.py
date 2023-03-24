from flask import jsonify, request
from src import db
from src.user import user_blueprint
from src.user.model import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)


@user_blueprint.get('/ping')
def ping():
    return jsonify('OK')


@user_blueprint.post('/signup')
def signup():
    email = request.json.get("email")
    password = request.json.get("password")
    if (not email or not password):
        return jsonify({'success': False, 'message': 'please provide email and password'})

    try:
        user = User.query.filter_by(email=email).one_or_none()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

    if (user):
        return jsonify({'success': False, 'message': 'user with email=[{}] already present'.format(email)})
    password = generate_password_hash(password)
    new_user = User(email=email, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

    return jsonify({'success': True, 'message': 'User created successfully'})


@user_blueprint.post("/login")
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    if (not email or not password):
        return jsonify({'success': False, 'message': 'please provide email and password'})

    try:
        user = User.query.filter_by(email=email).one_or_none()
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    if (not user):
        return jsonify({'success': False, 'message': 'user with email=[{}] not present. Do Signup first.'.format(email)})

    if not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Incorrect password'})

    return jsonify({
        "success": True,
        "user": {
            "refresh_token": create_refresh_token(identity=user.id),
            "access_token": create_access_token(identity=user.id)
        }
    })

# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@user_blueprint.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    return jsonify({
        "success": True,
        "user": {
            "access_token": create_access_token(identity=identity)
        }
    })


@user_blueprint.get("/whoami")
@jwt_required()
def whoami():
    identity = get_jwt_identity()
    if (identity):
        return jsonify({"success": True, "user_id": identity})
    else:
        return jsonify({"success": False})
