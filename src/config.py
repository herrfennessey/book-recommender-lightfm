from pathlib import Path


class Config:
    DEBUG = False
    TESTING = False
    BASE_DIR = Path(__file__).resolve().parent.parent
    PROFILE_MODEL_PATH = BASE_DIR / "model/profile"
    BOOKS_MODEL_PATH = BASE_DIR / "model/books"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    PROFILE_MODEL_PATH = Config.BASE_DIR / "model_test/profile"
    BOOKS_MODEL_PATH = Config.BASE_DIR / "model_test/books"
