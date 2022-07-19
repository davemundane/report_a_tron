import requests
import json
import config


rapid_seven_app_mapping = {"4ac0433a-532e-4cd3-a07d-5a192a740b0a": "Group Public Website", "9c123581-5a43-4986-9c97-39481840e5f7": "Bahamas Public Website", "ca4dcea9-8bf4-4c78-8af8-615786071b9d": "Bermuda Public Website", "4b6fe167-61d4-472f-9a1a-c4a40ddb6696": "Cayman Public Website", "5d427103-386f-43c5-b431-f43eca1d4fdf": "Channel Islands Public Website", "8a03bd4e-105c-4629-820d-c068a990e1db": "Channel Islands Public Website", "8a03bd4e-105c-4629-820d-c068a990e1db": "Guernsey Public Website", "0f59f624-f0ef-4f63-8f2f-5f6fe82c266e": "Jersey Public Website", "6fcb1c61-85b5-41ac-bf13-ef9c5f5b29fd": "Singapore Public Website", "f9c92048-b5f0-40dc-8e30-a06b290587e8": "Switzerland Public Website", "b5474e2f-ac52-4521-a537-ed63cfae2823": "UK Public Website", "53fc8536-b1de-4ad0-85e7-05315b632743": "Asset Management Public Website", "b702afed-75cb-493e-a6f8-356116133ec4": "Investors Public Website", "b8613142-1aa6-4cae-aa5e-d0011c261fd0": "Online Banking Bermuda/Cayman OBDX", "6da0ce17-92fc-47cc-90df-52368d26f445": "T24 (Temenos)", "646fa9b8-e08b-4a24-8334-83cefa637117": "OBDX Corporate"}

config_values = config.StaticValues().config_file
r7_url = config_values['r7_url']
elastic_url = config_values['elastic_url_base']
r7_headers = {"X-Api-Key": config_values['rapid7_apikey']}
elastic_headers = {"Content-Type": "application/json", "Authorization": "Basic " + config_values['reportatron_service_user']}
rapid7_get_vulns = requests.get(r7_url, headers = r7_headers)


sender = requests.post(elastic_url + "/insight_appsec/_delete_by_query", headers = elastic_headers, data = json.dumps({"query": {"match_all": {}}}))
sender = requests.post(elastic_url + "/consolidated_view/_delete_by_query", headers = elastic_headers, data = json.dumps({"query": {"match_all": {}}}))

for vuln in rapid7_get_vulns.json()['data']:

	app_id = vuln['app']['id']
	app_name = rapid_seven_app_mapping[app_id]

	vuln.update({"app": {"app_name": app_name, "id": app_id}})
	sender = requests.post(elastic_url + "/insight_appsec/_doc", headers = elastic_headers, data = json.dumps(vuln))

	if vuln['status'] == "VERIFIED":
		if vuln['severity'] == "CRITICAL":
			issue_rating = "Critical"
		elif vuln['severity'] == "HIGH":
			issue_rating = "High"
		elif vuln['severity'] == "MEDIUM":
			issue_rating = "Medium"
		elif vuln['severity'] == "LOW":
			issue_rating = "Low"
		else:
			vuln['severity'] = "Info"

		application_data = {"app_name": app_name, "issue_title": vuln['variances'][0]['attack']['id'], "issue_rating": issue_rating}
		sender = requests.post(elastic_url + "/consolidated_view/_doc", headers = elastic_headers, data = json.dumps(application_data))


for application_id in rapid_seven_app_mapping:

	application_name = rapid_seven_app_mapping[application_id]
	reportatron_query = json.dumps({"query": {"bool": {"must": [{"exists": {"field": "issue_stuff"}}, {"term": {"asset_stuff.asset_name.keyword": application_name}}, {"term": {"issue_stuff.issue_status.keyword": "Open"}}]}}})
	sender = requests.get(elastic_url + "/reportatron/_search", headers = elastic_headers, data = reportatron_query)
	reportatron_data = sender.json()['hits']['hits']

	for vuln in reportatron_data:

		application_data = {"app_name": application_name, "issue_title": vuln['_source']['issue_stuff']['issue_title'], "issue_rating": vuln['_source']['issue_stuff']['issue_risk_rating'], "issue_date": vuln['_source']['issue_stuff']['issue_created_on'], "issue_due_date": vuln['_source']['issue_stuff']['issue_due_date']}
		sender = requests.post(elastic_url + "/consolidated_view/_doc", headers = elastic_headers, data = json.dumps(application_data))
