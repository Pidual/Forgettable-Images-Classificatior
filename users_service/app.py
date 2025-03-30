from flask import Flask
from routes import user_routes
from db import init_db

app = Flask(__name__)

# Configurar la base de datos y JWT
app.config.from_object('config')
init_db(app)

# Registrar rutas
app.register_blueprint(user_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
