# users_service/app.py
from flask import Flask
from config import Config
from db import init_db
from routes import user_routes  # your blueprint
from models import User  # your model

app = Flask(__name__)
app.config.from_object(Config)
init_db(app)
app.register_blueprint(user_routes)

# Create tables if they don't exist
with app.app_context():
    from db import db  # Import the db instance
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

