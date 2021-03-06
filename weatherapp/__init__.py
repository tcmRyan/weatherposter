from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import conf

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object('conf.Config')
db = SQLAlchemy(app)

import weatherapp.exampleapp