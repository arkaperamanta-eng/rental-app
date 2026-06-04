import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # SQLite default
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///{base}/app.db".format(base=BASE_DIR.replace("\\", "/")),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

