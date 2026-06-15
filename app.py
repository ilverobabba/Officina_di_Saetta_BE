from flask import Flask
from flask_cors import CORS

from controller.auth_controller import auth_bp
from controller.engine_controller import engine_bp
from controller.car_model_controller import car_model_bp
from controller.optional_controller import optional_bp
from controller.compatibility_controller import compatibility_bp
from controller.configuration_controller import configuration_bp
from controller.quote_controller import quote_bp
from persistence.db_config import init_db

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(engine_bp)
app.register_blueprint(car_model_bp)
app.register_blueprint(optional_bp)
app.register_blueprint(compatibility_bp)
app.register_blueprint(configuration_bp)
app.register_blueprint(quote_bp)

init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
