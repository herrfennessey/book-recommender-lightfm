import logging.config
from datetime import datetime
from os import path

from flask import Flask, current_app, jsonify, make_response, request

from src.config import ProductionConfig, TestingConfig
from src.models.api import (
    ItemToItemRecommendationsRequest,
    UserToItemRecommendationsRequest,
)
from src.models.books_model import BooksModel
from src.models.item_to_item_model import ItemToItemModel
from src.models.user_to_item_model import UserToItemModel
from src.service.item_to_item import get_item_to_item_recommendations
from src.service.user_to_item import get_user_to_item_recommendations

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
        current_app.user_to_item = UserToItemModel.load_from_compressed_files(
            app.config["USER_TO_ITEM_PATH"]
        )
        current_app.item_to_item = ItemToItemModel.load_from_compressed_files(
            app.config["ITEM_TO_ITEM_PATH"]
        )
        current_app.book_model = BooksModel.load_from_compressed_files(
            app.config["BOOKS_MODEL_PATH"]
        )
        end = datetime.now()
        logging.info(
            f"Loaded pickle files in {round((end - start).total_seconds() * 1000)} milliseconds"
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
        return jsonify(current_app.user_to_item.info)

    @app.route("/user-to-item/predict", methods=["POST"])
    def user_to_item_predict():
        try:
            req = UserToItemRecommendationsRequest.model_validate(request.json)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 400)

        try:
            predictions = get_user_to_item_recommendations(
                user_id=str(req.user_id),
                genre_list=req.genres,
                n=req.limit,
            )
            return make_response(jsonify(predictions), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @app.route("/item-to-item/predict", methods=["POST"])
    def item_to_item_predict():
        try:
            req = ItemToItemRecommendationsRequest.model_validate(request.json)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 400)

        try:
            predictions = get_item_to_item_recommendations(
                work_id=str(req.work_id),
                n=req.limit,
            )
            return make_response(jsonify(predictions), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    return app
