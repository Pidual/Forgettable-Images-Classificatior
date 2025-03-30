import os
from flask import Blueprint, request, jsonify
import jwt
from config import Config
from inference import predict

inference_routes = Blueprint("inference", __name__)

# Middleware para validar JWT
def token_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            return func(*args, **kwargs, user_id=data["user_id"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
    return wrapper

# Endpoint para hacer inferencia sobre una imagen subida
@inference_routes.route("/predict/<int:image_id>", methods=["GET"])
@token_required
def classify_image(image_id, user_id):
    image_path = f"uploads/{user_id}/{image_id}.jpg"  # Ajustar si hay otra extensión
    if not os.path.exists(image_path):
        return jsonify({"message": "Image not found"}), 404

    prediction = predict(image_path)
    return jsonify({"prediction": prediction})
