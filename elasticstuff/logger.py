import json
import requests
import config
from elasticstuff import login
import datetime

class Logger:

	def __init__(self):

		config_values = config.StaticValues().config_file
		self.url = config_values['elastic_logging_url']
		self.headers = {"Content-Type": "application/json", "Authorization": "Basic " + config_values['reportatron_service_user']}
		self.sess = requests.Session()

	def createLog(self, event_detail, username):

		timestamp = datetime.datetime.now().isoformat().split(".")[0]
		body = json.dumps({"doc": {"activity_log": {"user": username, "time": timestamp, "event_detail": event_detail}}})
		sender = self.sess.post(self.url + "_doc/", headers=self.headers, data=body)

		if sender.status_code != 201:
		    raise ReferenceError('update failed')
