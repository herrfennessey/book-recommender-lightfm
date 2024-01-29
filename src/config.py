from pathlib import Path


class Config:
    DEBUG = False
    TESTING = False
    BASE_DIR = Path(__file__).resolve().parent.parent
    USER_TO_ITEM_PATH = BASE_DIR / "model/user_to_item"
    ITEM_TO_ITEM_PATH = BASE_DIR / "model/item_to_item"
    BOOKS_MODEL_PATH = BASE_DIR / "model/books"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    USER_TO_ITEM_PATH = Config.BASE_DIR / "model_test/profile"
    ITEM_TO_ITEM_PATH = Config.BASE_DIR / "model_test/item_to_item"
    BOOKS_MODEL_PATH = Config.BASE_DIR / "model_test/books"
