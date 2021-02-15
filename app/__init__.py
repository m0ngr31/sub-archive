from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__,
  static_url_path='/static',
  static_folder = "../static",
  template_folder = "../templates"
)

app.config.from_object(Config)
db = SQLAlchemy(app)

from app import models, routes
