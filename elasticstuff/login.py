import requests
import json
import bcrypt
from flask_login import UserMixin
import config

class User(UserMixin):
    pass

class Login:

    def __init__(self):

        config_values = config.StaticValues().config_file
        self.url = config_values['elastic_users']
        self.auth_value = config_values['reportatron_service_user']
        self.headers = {"Content-Type": "application/json", "Authorization": "Basic " + self.auth_value}
        self.sess = requests.Session()

    def checkUserExists(self, username):

        user_query = json.dumps({"size": 0, "query": {"bool": {"must": {"exists": {"field": str(username)}}}}})

        sender = self.sess.get(self.url + "_search", data=user_query, headers=self.headers)
        if sender.json()['hits']['total']['value'] == 1:
            return True
        else:
            return False

    def createUser(self, username, password):

        hashed_password = self.hashPassword(password)
        body = json.dumps({username: {"password": hashed_password}})

        sender = self.sess.post(self.url + "_doc", data=body, headers=self.headers)

        if sender.status_code != 201:
            raise ReferenceError('user not created')

    def updateUser(self, username, password):

        hashed_password = self.hashPassword(password)
        body = json.dumps({"doc": {username: {"password": hashed_password.decode('utf8')}}})

        doc_id_query = json.dumps({"query": {"bool": {"must": {"exists": {"field": str(username)}}}}})
        doc_id = self.sess.post(self.url + "_search", data=doc_id_query, headers=self.headers).json()['hits']['hits'][0]['_id']
        sender = self.sess.post(self.url + "_update/" + str(doc_id), data=body, headers=self.headers)

    def hashPassword(self, password):

        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12))
        return hashed_password

    def comparePassword(self, username, password):

        user_query = json.dumps({"query": {"bool": {"must": {"exists": {"field": str(username)}}}}})
        sender = self.sess.get(self.url + "_search", data=user_query, headers=self.headers)
        hashed_password = sender.json()['hits']['hits'][0]['_source'][username]['password']
        password_check = bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))
        return password_check

    def checkForOtp(self,username):

        user_query = json.dumps({"query": {"bool": {"must": {"exists": {"field": str(username)}}}}})
        sender = self.sess.get(self.url + "_search", data=user_query, headers=self.headers)

        if sender.json()['hits']['hits'][0]['_source'][username]['has_otp'] == "Yes":
            return {"user_otp": True, "secret": sender.json()['hits']['hits'][0]['_source'][username]['otp_secret']}
        else:
            return {"user_otp": False, "secret": None}

    def getUserSecret(self,username):

        user_query = json.dumps({"query": {"bool": {"must": {"exists": {"field": str(username)}}}}})
        sender = self.sess.get(self.url + "_search", data=user_query, headers=self.headers)

        if sender.json()['hits']['hits'][0]['_source'][username]['otp_secret']:
            return sender.json()['hits']['hits'][0]['_source'][username]['otp_secret']
        else:
            return False

    def updateOtpStatus(self, username):

        user_query = json.dumps({"query": {"bool": {"must": {"exists": {"field": str(username)}}}}})
        sender = self.sess.get(self.url + "_search", data=user_query, headers=self.headers)
        doc_id = sender.json()['hits']['hits'][0]['_id']

        update_user = json.dumps({"doc": {str(username): {"has_otp": "Yes"}}})
        sender = self.sess.post(self.url + "_update/" + str(doc_id), data=update_user, headers=self.headers)

        if sender.json()['result'] == "updated":
            return True
        else:
            return False

    def updateOtpSecret(self, username, secret_token):

        user_query = json.dumps({"query": {"bool": {"must": {"exists": {"field": str(username)}}}}})
        sender = self.sess.get(self.url + "_search", data=user_query, headers=self.headers)
        doc_id = sender.json()['hits']['hits'][0]['_id']

        update_user = json.dumps({"doc": {str(username): {"otp_secret": secret_token}}})
        sender = self.sess.post(self.url + "_update/" + str(doc_id), data=update_user, headers=self.headers)

        if sender.json()['result'] == "updated":
            return True
        else:
            return False

    def getPermissions(self, username):

        user_query = json.dumps({"query": {"bool": {"must": {"exists": {"field": str(username)}}}}})
        sender = self.sess.get(self.url + "_search", data=user_query, headers=self.headers)
        user_document = sender.json()['hits']['hits'][0]['_source']

        return user_document[username]['user_role']
