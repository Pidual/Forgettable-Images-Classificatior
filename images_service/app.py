# images_service/app.py
from flask import Flask
from routes import image_routes
from db import init_db

app = Flask(__name__)

# Configuración
app.config.from_object("config.Config")
init_db(app)

# Registrar rutas
app.register_blueprint(image_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
