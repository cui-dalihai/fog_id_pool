from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "FOG_ID"
app.config["MONGO_HOST"] = '127.0.0.1'
app.config["MONGO_PORT"] = 27017

mongo = PyMongo()

mongo.init_app(app)
with app.app_context():
    mongo.db['fog_id'].create_index('FogID', background=True, unique=True)

APP_URL = "http://127.0.0.1:5000"
