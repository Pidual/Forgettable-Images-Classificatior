# images_service/routes.py
import os
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
import jwt
from models import db, Image
from config import Config
import functools

image_routes = Blueprint("images", __name__)

# Función para verificar archivos permitidos
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Middleware para validar JWT
def token_required(func):
    @functools.wraps(func)
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


# Endpoint para subir imágenes
@image_routes.route("/upload", methods=["POST"])
@token_required
def upload_image(user_id):
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"message": "Invalid file"}), 400

    filename = secure_filename(file.filename)
    
    # Crear carpeta por usuario
    user_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], str(user_id))
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    file_path = os.path.join(user_folder, filename)
    file.save(file_path)

    new_image = Image(user_id=user_id, image_path=file_path)
    db.session.add(new_image)
    db.session.commit()

    return jsonify({"message": "File uploaded", "image_id": new_image.id}), 201


# Endpoint para ver imágenes
@image_routes.route("/images/<int:image_id>", methods=["GET"])
@token_required
def get_image(image_id, user_id):
    image = Image.query.filter_by(id=image_id, user_id=user_id).first()
    if not image:
        return jsonify({"message": "Image not found"}), 404

    # Extraer la carpeta del usuario y el archivo
    user_folder = os.path.join(current_app.config["UPLOAD_FOLDER"], str(user_id))
    return send_from_directory(user_folder, os.path.basename(image.image_path))

