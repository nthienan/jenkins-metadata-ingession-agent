import json
import logging
import requests
import time


class Elasticsearch:

    def __init__(self, url):
        self.url = url
        logging.debug("Initilized Elasticsearch client at %s" % url)

    def store(self, data):
        start = time.perf_counter()
        url = self.url + '/_bulk'
        headers = {"Content-Type": "application/x-ndjson"}
        payload = '\n'.join([json.dumps(item) for item in data]) + '\n'

        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        error = bool(response.json()["errors"])
        if error:
            logging.warning("Couldn't store data into Elasticsearch due to %s" % response.json())
            raise Exception("Couldn't store data into Elasticsearch", response.json())

        logging.debug("Store data into Elasticsearch successfully. It took %.3f seconds" % round(time.perf_counter()- start, 3))

        return response

    def query(self, target, query):
        start = time.perf_counter()
        url = f"{self.url}/{target}/_search"
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, data=query, headers=headers)
        response.raise_for_status()

        logging.debug("Query data from Elasticsearch successfully. It took %.3f seconds" % round(time.perf_counter()- start, 3))
        return response
