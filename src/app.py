from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException, default_exceptions
import logging
import argparse
import sys
import yaml
import os
from argparse import Action

from endpoints.build import Build

class EnvAction(Action):
    def __init__(self, env, required=True, default=None, **kwargs):
        if not default and env:
            if env in os.environ:
                default = os.environ[env]
        if required and default:
            required = False
        super(EnvAction, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def parse_opts(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config-file", env="JMIA_CONFIG_FILE", dest="cfg_file", action=EnvAction,
                        help="Location of configuration file")

    return parser.parse_args(args)


def init_logger(level="INFO"):
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


def init_error_handler(app, error_handler):
    for ex in default_exceptions:
        app.register_error_handler(ex, error_handler)

    api = Api(app)
    api.prefix = "/api"

    api.add_resource(Build, "/builds")


app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


if __name__ == "__main__":
    opts = parse_opts(sys.argv[1:])

    if not os.path.exists(opts.cfg_file):
        raise RuntimeError("\"%s\" does not exist" % opts.cfg_file)
    with open(opts.cfg_file) as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    init_logger(cfg["logging"]["level"])
    init_error_handler(app, handle_error)

    app.config.update(cfg)
    app.run()
