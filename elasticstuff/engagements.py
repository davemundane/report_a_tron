import json
import requests
import config


class Engagements:

	def __init__(self):

		config_values = config.StaticValues().config_file
		self.url = config_values['elastic_url']
		self.headers = {"Content-Type": "application/json", "Authorization": "Basic " + config_values['reportatron_service_user']}
		self.sess = requests.Session()

	def getEngagements(self):

		body = json.dumps({"size": 10000, "query": {"bool": {"filter": {"term": {"doc_type": "engagement"}}}}, "sort": [{"engagement_stuff.engagement_received_on": {"order": "desc"}}]})

		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data

	def createEngagement(self, asset_name_list, linked_assets, engagement_form_location, engagement_main_contact, engagement_risk_rating, engagement_received_on, engagement_action_taken,  engagement_notes):

		body = json.dumps({"doc_type": "engagement", "engagement_stuff": {"engagement_has_assets": linked_assets, "engagement_has_asset_names": asset_name_list, "engagement_form_location": engagement_form_location, "engagement_main_contact": engagement_main_contact, "engagement_risk_rating": engagement_risk_rating, "engagement_received_on": engagement_received_on, "engagement_action_taken": engagement_action_taken, "engagement_notes": engagement_notes, "engagement_status": "Open"}})

		sender = self.sess.post(self.url + "_doc", data=body, headers=self.headers)
		if sender.status_code != 201:
			raise ReferenceError('engagement not created')

	def getEngagementsForAsset(self, asset_id):

		body = json.dumps({"size":10000, "query": {"bool": {"must": {"match": {"engagement_stuff.engagement_has_assets.keyword": asset_id}}}}})

		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data

	def updateengagementapi(self, asset_name_list, linked_assets, engagement_id, engagement_form_location, engagement_main_contact, engagement_risk_rating, engagement_received_on, engagement_action_taken,  engagement_notes, engagement_status):

		body = json.dumps({"doc": {"doc_type": "engagement", "engagement_stuff": {"engagement_has_assets": linked_assets, "engagement_has_asset_names": asset_name_list, "engagement_form_location": engagement_form_location, "engagement_main_contact": engagement_main_contact, "engagement_risk_rating": engagement_risk_rating, "engagement_received_on": engagement_received_on, "engagement_action_taken": engagement_action_taken, "engagement_notes": engagement_notes, "engagement_status": engagement_status}}})

		sender = self.sess.post(self.url + "_update/" + engagement_id, headers=self.headers, data=body)

		if sender.status_code != 200:
			raise ReferenceError('update failed')

	def getOpenEngagements(self):

		body = json.dumps({"size":10000, "query": {"bool": {"must": {"match": {"engagement_stuff.engagement_status.keyword": "Open"}}}},"sort": [{"engagement_stuff.engagement_received_on": {"order": "desc"}}]})

		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data
