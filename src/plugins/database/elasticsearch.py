import json
import logging
import requests


class Elasticsearch:

    def __init__(self, url):
        self.url = url
        logging.info("Initilized Elasticsearch client at %s" % url)

    def store(self, data):
        url = self.url + '/_bulk'
        headers = {"Content-Type": "application/x-ndjson"}
        payload = '\n'.join([json.dumps(item) for item in data]) + '\n'

        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        error = bool(response.json()["errors"])
        if error:
            raise Exception("Couldn't store into Elasticsearch", response.json())

        return response
