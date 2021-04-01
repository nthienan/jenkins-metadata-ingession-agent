import logging
from flask_restful import Resource
from flask import request, current_app
from datetime import datetime, timezone
import uuid

from plugins.database.elasticsearch import Elasticsearch


class Build(Resource):

    def __init__(self):
        self._index_pattern = current_app.config["elasticsearch"]["index-pattern"]["build-metadata"]
        self.elasticsearch = Elasticsearch(current_app.config["elasticsearch"]["url"])

    def post(self):
        data = request.json
        logging.info(data)

        data["id"] = str(uuid.uuid4())
        data["time"] = datetime.fromtimestamp(int(data["timestamp"]), timezone.utc).isoformat()

        payload = [self._build_metadata(data), data]
        self.elasticsearch.store(payload)

        return {"status": "Successful"}, 201

    def _build_metadata(self, data: dict):
        metadata = {"index": {}}

        timestamp = int(data["timestamp"])
        time_pattern = datetime.fromtimestamp(timestamp).strftime("%Y-%m")

        metadata["index"]["_index"] = "%s-%s" % (self._index_pattern, time_pattern)
        metadata["index"]["_id"] = data["id"]
        return metadata
