from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.from_object('snitch.config')
db = SQLAlchemy(app)

from snitch.api import api
