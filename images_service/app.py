# images_service/app.py
from flask import Flask
from routes import image_routes
from db import init_db, db  # import the db instance as well
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
init_db(app)

# Register routes
app.register_blueprint(image_routes)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

