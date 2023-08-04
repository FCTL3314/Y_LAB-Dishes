import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.environ.get("DEBUG")

    DISH_PRICE_ROUNDING = os.environ.get("DISH_PRICE_ROUNDING")

    DATABASE_NAME = os.environ.get("DATABASE_NAME")
    DATABASE_HOST = os.environ.get("DATABASE_HOST")
    DATABASE_PORT = os.environ.get("DATABASE_PORT")
    DATABASE_USER = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

    REDIS_HOST = os.environ.get("REDIS_HOST")
    REDIS_PORT = os.environ.get("REDIS_PORT")
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"


class TestConfig(Config):
    DATABASE_NAME = os.environ.get("TEST_DATABASE_NAME")
    DATABASE_HOST = os.environ.get("TEST_DATABASE_HOST")
    DATABASE_PORT = os.environ.get("TEST_DATABASE_PORT")
    DATABASE_USER = os.environ.get("TEST_DATABASE_USER")
    DATABASE_PASSWORD = os.environ.get("TEST_DATABASE_PASSWORD")
