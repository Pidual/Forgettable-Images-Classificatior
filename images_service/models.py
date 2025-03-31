# images_services/models.py
from db import db

class Image(db.Model): # crea los campos
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Se validará con JWT
    image_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
