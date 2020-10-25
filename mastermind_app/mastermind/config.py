import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Config(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    TESTING = True
