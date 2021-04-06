import json
import logging
from flask_restful import Resource
from flask import request, current_app
from datetime import datetime, timezone
import uuid

from plugins.database.elasticsearch import Elasticsearch


class Build(Resource):

    def __init__(self):
        self._index_pattern = current_app.config["elasticsearch"]["index-pattern"]["build-metadata"]
        self.elasticsearch = Elasticsearch(
            current_app.config["elasticsearch"]["url"])

    def get(self):
        folder = request.args.get("folder")
        period = request.args.get("period")
        status = request.args.get("status")

        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "repoOwner": {
                                    "query": f"{folder}"
                                }
                            }
                        },
                        {
                            "bool": {
                                "should": []
                            }
                        },
                        {
                            "range": {
                                "time": {
                                    "from": f"now-{period}m",
                                    "to": "now"
                                }
                            }
                        }
                    ]
                }
            }
        }

        query["query"]["bool"]["must"][1]["bool"]["should"] = list(map(lambda s: {
            "match": {
                "result": {
                    "query": f"{s}"
                }
            }
        }, status.split(",")))

        response = self.elasticsearch.query(f"{self._index_pattern}-*", json.dumps(query))
        data = list(map(lambda i: i["_source"], response.json()["hits"]["hits"]))
        return data, 200

    def post(self):
        data = request.json
        logging.info(data)

        data["id"] = str(uuid.uuid4())
        data["time"] = datetime.fromtimestamp(
            int(data["timestamp"]), timezone.utc).isoformat()

        payload = [self._build_metadata(data), data]
        self.elasticsearch.store(payload)

        return {"status": "Successful"}, 201

    def _build_metadata(self, data: dict):
        metadata = {"index": {}}

        timestamp = int(data["timestamp"])
        time_pattern = datetime.fromtimestamp(timestamp).strftime("%Y-%m")

        metadata["index"]["_index"] = "%s-%s" % (
            self._index_pattern, time_pattern)
        metadata["index"]["_id"] = data["id"]
        return metadata
