import requests
import json
import config

class Reports:

    def __init__(self):

        config_values = config.StaticValues().config_file
        self.url = config_values['elastic_url']
        self.headers = {"Content-Type": "application/json", "Authorization": "Basic " + config_values['reportatron_service_user']}
        self.sess = requests.Session()

    def getTestData(self, test_id):

        test_data =  self.sess.get(self.url + "_doc/" + test_id, headers=self.headers)

        return test_data.json()


    def getIssueData(self, test_id):

        issue_query = json.dumps({"size": 1000, "query": {"match": {"issue_stuff.issue_has_tests.keyword": test_id}}})

        issue_report_data = self.sess.get(self.url + "_search", headers=self.headers, data=issue_query)

        return issue_report_data.json()['hits']['hits']

    def getAssetData(self, asset_id):

        asset_data =  self.sess.get(self.url + "_doc/" + asset_id, headers=self.headers)

        return asset_data.json()

    def getServiceData(self, service_id):

        service_data =  self.sess.get(self.url + "_doc/" + service_id, headers=self.headers)

        return service_data.json()

    def getIssuesForAsset(self, asset_id):

        issue_query = json.dumps({"size": 1000, "query": {"match": {"issue_stuff.issue_has_assets.keyword": asset_id}}})

        issue_report_data = self.sess.get(self.url + "_search", headers=self.headers, data=issue_query)

        return issue_report_data.json()['hits']['hits']

    def getTestsForAsset(self, asset_id):

        test_query = json.dumps({"size": 1000, "query": {"match": {"test_stuff.test_has_assets.keyword": asset_id}}})

        test_report_data = self.sess.get(self.url + "_search", headers=self.headers, data=test_query)

        return test_report_data.json()['hits']['hits']
