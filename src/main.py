import logging.config
from datetime import datetime
from os import path

from flask import Flask, current_app, jsonify, make_response, request

from src.config import ProductionConfig, TestingConfig
from src.models.api import ProfileRecommendationsRequest
from src.models.books_model import BooksModel
from src.models.profile_model import ProfileModel
from src.service.profile_service import get_predictions

# setup loggers to display more information
log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)


def create_app(test: bool = False):
    app = Flask(__name__)

    if test:
        config = TestingConfig
    else:
        config = ProductionConfig

    app.config.from_object(config)

    with app.app_context():
        start = datetime.now()
        current_app.profile_model = ProfileModel.load_from_pickle(
            app.config["PROFILE_MODEL_PATH"]
        )
        current_app.book_model = BooksModel.load_from_pickle(
            app.config["BOOKS_MODEL_PATH"]
        )
        end = datetime.now()
        logging.info(
            f"Loaded pickle files in {(end - start).microseconds / 1000} milliseconds"
        )

    # Register routes
    @app.route("/")
    def hello_world():
        return jsonify({"message": "Hello World!"})

    @app.route("/health")
    def health():
        return jsonify({"status": "Healthy"})

    @app.route("/model-info")
    def model_info():
        return jsonify(current_app.profile_model.info)

    @app.route("/predict", methods=["POST"])
    def profile_predict():
        try:
            req = ProfileRecommendationsRequest.model_validate(request.json)
        except Exception as e:
            return make_response(jsonify(e), 400)

        try:
            predictions = get_predictions(
                user_id=str(req.user_id),
                genre_list=req.genres,
                n=req.limit,
            )
            return make_response(jsonify(predictions), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    return app
