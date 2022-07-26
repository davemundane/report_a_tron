import json
import requests
import config


class Docs:

	def __init__(self):

		config_values = config.StaticValues().config_file
		self.url = config_values['elastic_url']
		self.headers = {"Content-Type": "application/json", "Authorization": "Basic " + config_values['reportatron_service_user']}
		self.sess = requests.Session()

	def getDoc(self, doc_id):

		sender = self.sess.get(self.url + "_doc/" + doc_id, headers=self.headers)
		data = sender.json()

		return data

	def getAssets(self):

		body = json.dumps({"_source": "asset_stuff.asset_name", "size": 10000, "query": {"bool": {"filter": {"term": {"doc_type": "asset"}}}}, "sort": [{"asset_stuff.asset_created_on": {"order": "desc"}}]})
		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)

		return sender.json()['hits']['hits']
