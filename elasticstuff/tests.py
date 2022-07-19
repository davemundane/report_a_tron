import json
import requests
import config


class Tests:

	def __init__(self):

		config_values = config.StaticValues().config_file
		self.url = config_values['elastic_url']
		self.headers = {"Content-Type": "application/json", "Authorization": "Basic " + config_values['reportatron_service_user']}
		self.sess = requests.Session()

	def getTests(self):

		body = json.dumps({"size": 10000, "query": {"bool": {"filter": {"term": {"doc_type": "test"}}}}, "sort": [{"test_stuff.test_date": {"order": "desc"}}]})
		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data

	def createtestapi(self, asset_list, asset_name_list, engagement_id, test_type, test_exec_summary, test_base_location, test_limitations, test_main_contact, test_created_on, test_date, test_notes):

		#print(asset_list, asset_name_list, engagement_id, test_type, test_exec_summary, test_base_location, test_limitations, test_main_contact, test_created_on, test_date, test_notes)

		body = {"doc_type": "test", "test_stuff": {"test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_created_on": test_created_on, "test_date": test_date, "test_notes": test_notes}}

		#print(body)

		if asset_list:
			body.update({"doc_type": "test", "test_stuff": {"test_has_assets": asset_list, "test_has_asset_names": asset_name_list, "test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_created_on": test_created_on, "test_date": test_date, "test_notes": test_notes}})

			if engagement_id:
				body.update({"doc_type": "test", "test_stuff": {"test_has_engagements": [engagement_id], "test_has_assets": asset_list, "test_has_asset_names": asset_name_list, "test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_created_on": test_created_on, "test_date": test_date, "test_notes": test_notes}})

			else:
				body.update({"doc_type": "test", "test_stuff": {"test_has_assets": asset_list, "test_has_asset_names": asset_name_list, "test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_created_on": test_created_on, "test_date": test_date, "test_notes": test_notes}})

		body = json.dumps(body)
		#print(body)

		sender = self.sess.post(self.url + "_doc", data=body, headers=self.headers)
		#print(sender.json())
		if sender.status_code != 201:
			raise ReferenceError('test not created')

	def getTestsForEngagement(self, engagement_id):

		body = json.dumps({"size":10000, "query": {"bool": {"must": [{"match": {"test_stuff.test_has_engagements": engagement_id}}]}}})
		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data

	def getTestsForAsset(self, asset_id):

		body = json.dumps({"size":10000, "query": {"bool": {"must": [{"match": {"test_stuff.test_has_assets": asset_id}}]}}})
		sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
		data = sender.json()['hits']['hits']

		return data

	def updateTest(self, asset_list, asset_name_list, engagement_id, test_id, test_type, test_exec_summary, test_base_location, test_limitations, test_main_contact, test_date, test_notes):

		body = {"doc": {"doc_type": "test", "test_stuff": {"test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_date": test_date, "test_notes": test_notes}}}

		if asset_list:
			body.update({"doc": {"doc_type": "test", "test_stuff": {"test_has_assets": asset_list, "test_has_asset_names": asset_name_list, "test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_date": test_date, "test_notes": test_notes}}})

			if engagement_id:
				body.update({"doc": {"doc_type": "test", "test_stuff": {"test_has_assets": asset_list, "test_has_asset_names": asset_name_list, "test_has_engagements": [engagement_id], "test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_date": test_date, "test_notes": test_notes}}})

		elif engagement_id:
			body.update({"doc": {"doc_type": "test", "test_stuff": {"test_has_engagements": [engagement_id], "test_type": test_type, "test_exec_summary": test_exec_summary, "test_base_location": test_base_location, "test_limitations": test_limitations, "test_main_contact": test_main_contact, "test_date": test_date, "test_notes": test_notes}}})

		body = json.dumps(body)

		sender = self.sess.post(self.url + "_update/" + test_id, headers=self.headers, data=body)

		if sender.status_code != 200:
			raise ReferenceError('update failed')
