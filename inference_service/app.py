from flask import Flask
from routes import inference_routes

app = Flask(__name__)
app.config.from_object("config")

app.register_blueprint(inference_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
