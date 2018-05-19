from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('snitch.config.config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from snitch.api import api
from snitch.batch.tree import get_tree_path
