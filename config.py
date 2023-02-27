import os

basedir = os.path.abspath(
    os.path.dirname(__file__))  # basedir reads out path of current file, so db is dropped in correct folder


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "1234"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
                              "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
