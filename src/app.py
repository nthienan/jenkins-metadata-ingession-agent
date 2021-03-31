from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException, default_exceptions
import logging

from endpoints.build import Build


app = Flask(__name__)

def init_logger(level="INFO"):
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


def init_error_handler(app, error_handler):
    for ex in default_exceptions:
        app.register_error_handler(ex, error_handler)

    api = Api(app)
    api.prefix = '/api'

    api.add_resource(Build, '/builds')


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


if __name__ == '__main__':
    init_logger()
    init_error_handler(app, handle_error)
    app.run()
