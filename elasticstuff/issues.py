import json
import requests
import config
import datetime

class Issues:

    def __init__(self):

        config_values = config.StaticValues().config_file
        self.url = config_values['elastic_url']
        self.headers = {"Content-Type": "application/json", "Authorization": "Basic " + config_values['reportatron_service_user']}
        self.sess = requests.Session()

    def getIssues(self):

        body = json.dumps({"size": 10000, "query": {"bool": {"filter": {"term": {"doc_type": "issue"}}}}, "sort": [{"issue_stuff.issue_created_on": {"order": "desc"}}]})
        sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
        data = sender.json()['hits']['hits']

        return data

    def getIssuesFilter(self, searchTerm):

        if searchTerm:

            if "test_id" in searchTerm:

                body = json.dumps({"size": 10000, "query": {"bool": {"filter": {"term": {"issue_stuff.issue_has_tests.keyword": searchTerm['test_id']}}}}})
                sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
                data = sender.json()['hits']['hits']

                return data

            elif "engagement_id" in searchTerm:

                body = json.dumps({"size": 10000, "query": {"bool": {"filter": {"term": {"issue_stuff.issue_has_engagements.keyword": searchTerm['engagement_id']}}}}})
                sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
                data = sender.json()['hits']['hits']

                return data

            elif "asset_id" in searchTerm:

                body = json.dumps({"size": 10000, "query": {"bool": {"filter": {"term": {"issue_stuff.issue_has_assets.keyword": searchTerm['asset_id']}}}}})
                sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
                data = sender.json()['hits']['hits']

                return data

        else:

            body = json.dumps({"size":10000, "query": {"bool": {"must": {"exists": {"field": "issue_stuff"}}}}})
            sender = self.sess.get(self.url + "_search", headers=self.headers, data=body)
            data = sender.json()['hits']['hits']

            return data

    def createissue(self, asset_list, asset_name_list, engagement_id, test_id, issue_title, issue_location, issue_description, issue_remediation, issue_risk_rating, issue_risk_impact, issue_risk_likelihood, issue_status, issue_details, issue_notes, timenow):

        issue_due_date = timenow
        if issue_risk_rating == "Critical":
            issue_due_date = timenow + datetime.timedelta(days=7)
        elif issue_risk_rating == "High":
            issue_due_date = timenow + datetime.timedelta(days=30)
        elif issue_risk_rating == "Medium":
            issue_due_date = timenow + datetime.timedelta(days=60)
        elif issue_risk_rating == "Low":
            issue_due_date = timenow + datetime.timedelta(days=180)
        else:
            issue_due_date = timenow + datetime.timedelta(days=10000)

        timenow = timenow.isoformat().split('T')[0]
        issue_due_date = issue_due_date.isoformat().split('T')[0]

        body = {"doc_type": "issue", "issue_stuff": {"issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_created_on": timenow, "issue_due_date": issue_due_date}}

        if test_id:

            if engagement_id:

                if asset_list:

                    body.update({"doc_type": "issue", "issue_stuff": {"issue_has_tests": [test_id], "issue_has_engagements": [engagement_id], "issue_has_assets": asset_list, "issue_has_asset_names": asset_name_list, "issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_created_on": timenow, "issue_due_date": issue_due_date}})

                else:
                    body.update({"doc_type": "issue", "issue_stuff": {"issue_has_tests": [test_id], "issue_has_engagements": [engagement_id], "issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_created_on": timenow, "issue_due_date": issue_due_date}})
            else:
                body.update({"doc_type": "issue", "issue_stuff": {"issue_has_tests": [test_id], "issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_created_on": timenow, "issue_due_date": issue_due_date}})
        else:
            body = {"doc_type": "issue", "issue_stuff": {"issue_has_assets": asset_list, "issue_has_asset_names": asset_name_list, "issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_created_on": timenow, "issue_due_date": issue_due_date}}

        body = json.dumps(body)

        sender = self.sess.post(self.url + "_doc", data=body, headers=self.headers)
        if sender.status_code != 201:
            raise ReferenceError('test not created')

    def updateIssue(self, asset_list, asset_name_list, issue_id, issue_title, issue_risk_rating, issue_risk_impact, issue_risk_likelihood, issue_location, issue_status, issue_description, issue_remediation, issue_details, issue_notes, issue_ra_date, issue_ra_owner, issue_ra_expiry, issue_ra_notes, issue_due_date):


        if asset_list:
            body = json.dumps({"doc": {"doc_type": "issue", "issue_stuff": {"issue_has_assets": asset_list, "issue_has_asset_names": asset_name_list, "issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_due_date": issue_due_date, "issue_ra_stuff": {"issue_ra_date": issue_ra_date, "issue_ra_owner": issue_ra_owner, "issue_ra_expiry": issue_ra_expiry, "issue_ra_notes": issue_ra_notes}}}})

        else:
            body = json.dumps({"doc": {"doc_type": "issue", "issue_stuff": {"issue_title": issue_title, "issue_location": issue_location, "issue_description": issue_description, "issue_remediation": issue_remediation, "issue_risk_rating": issue_risk_rating, "issue_risk_impact": issue_risk_impact, "issue_risk_likelihood": issue_risk_likelihood, "issue_status": issue_status, "issue_details": issue_details, "issue_notes": issue_notes, "issue_due_date": issue_due_date, "issue_ra_stuff": {"issue_ra_date": issue_ra_date, "issue_ra_owner": issue_ra_owner, "issue_ra_expiry": issue_ra_expiry, "issue_ra_notes": issue_ra_notes}}}})

        sender = self.sess.post(self.url + "_update/" + issue_id, headers=self.headers, data=body)
        if sender.status_code != 200:
            raise ReferenceError('update failed')


    def closeSingleIssue(self, issue_id):

        body = json.dumps({"doc": {"issue_stuff": {"issue_status": "Closed"}}})
        sender = self.sess.post(self.url + "_update/" + issue_id, headers=self.headers, data=body)

        if sender.status_code != 200:
            raise ReferenceError('update failed')
