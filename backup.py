import json
import requests
import config
import calendar
import datetime


config_values = config.StaticValues().config_file
url = config_values['elastic_url_base']
headers = {"Content-Type": "application/json", "Authorization": "Basic " + config_values['reportatron_service_user']}
sess = requests.Session()

day = datetime.datetime.today().day
month = datetime.datetime.today().month
year = datetime.datetime.today().year

snap_name = "reportatron_snap_" + str(day) + "_" + str(month) + "_" + str(year)

body = json.dumps({"indices": "reportatron", "ignore_unavailable": "true", "include_global_state": "false"})

reportatron_backup = sess.put(url + "_snapshot/s3_repository/" + snap_name + "?wait_for_completion=true", headers=headers, data=body)

snap_name = "reportatron_users_snap_" + str(day) + "_" + str(month) + "_" + str(year)

body = json.dumps({"indices": "reportatron_users", "ignore_unavailable": "true", "include_global_state": "false"})

reportatron_backup = sess.put(url + "_snapshot/s3_repository/" + snap_name + "?wait_for_completion=true", headers=headers, data=body)
