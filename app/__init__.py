from flask import jsonify
from app.view import search, get_detail_common
from flask import Flask, g
import config
from app.view.view import view
from app.upload.upload import upload
from flask_cors import CORS
from pymongo import MongoClient


def create_app(config_file=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_file)
    app.register_blueprint(view)
    app.register_blueprint(upload)
    CORS(app)
    client = MongoClient('localhost', 27017)
    db = client.exhentai

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.errorhandler(400)
    def page_not_found(e):
        return jsonify(msg=str(e)), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(msg=str(e)), 404

    return app

