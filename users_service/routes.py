from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from models import db, User
from config import Config

user_routes = Blueprint('users', __name__)

def generate_token(user_id, expires_in=8200):
    """Genera un token JWT para el usuario."""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    token = jwt.encode({"user_id": user_id, "exp": expiration}, Config.SECRET_KEY, algorithm="HS256")
    return token

@user_routes.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed_pw = generate_password_hash(data["password"], method="pbkdf2:sha256")
    new_user = User(username=data["username"], password_hash=hashed_pw, email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@user_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password_hash, data["password"]):
        token = generate_token(user.id)
        return jsonify({"token": token})
    return jsonify({"message": "Invalid credentials"}), 401
