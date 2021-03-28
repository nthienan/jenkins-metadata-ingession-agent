from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException, default_exceptions


app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


def initilze(app, error_handler):
    for ex in default_exceptions:
        app.register_error_handler(ex, error_handler)

    api = Api(app)
    api.prefix = '/api'

    # api.add_resource(BuildsResource, '/builds', '/users/<int:user_id>')


if __name__ == '__main__':
    initilze(app, handle_error)
    app.run(debug=True)
