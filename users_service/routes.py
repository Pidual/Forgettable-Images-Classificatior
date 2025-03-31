# users_service/routes.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from models import User
from db import db
from config import Config
from sqlalchemy.exc import IntegrityError

user_routes = Blueprint('users', __name__)

def generate_token(user_id, expires_in=8200):
    """Generate a JWT token for the user."""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    token = jwt.encode({"user_id": user_id, "exp": expiration}, Config.SECRET_KEY, algorithm="HS256")
    return token

@user_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed_pw = generate_password_hash(data["password"], method="pbkdf2:sha256")
    new_user = User(username=data["username"], password_hash=hashed_pw, email=data["email"])
    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()  # rollback the session to clean it
        return jsonify({"message": "Username already exists"}), 409
    return jsonify({"message": "User created"}), 201

@user_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password_hash, data["password"]):
        token = generate_token(user.id)
        return jsonify({"token": token})
    return jsonify({"message": "Invalid credentials"}), 401
