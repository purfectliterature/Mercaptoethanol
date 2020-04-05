import pickle
import requests
import os
import core.routes as routes
import core.parser as parser

class Session:
    DEFAULT_COOKIES_FILE = "session.mssn"

    @staticmethod
    def download(url, filename):
        blob = requests.get(url)
        with open(filename, "wb") as file:
            file.write(blob.content)
        return True
    
    def __init__(self):
        self.session = requests.Session()
        if (os.path.exists(Session.DEFAULT_COOKIES_FILE)):
            with open(Session.DEFAULT_COOKIES_FILE, "rb") as file:
                self.session.cookies.update(pickle.load(file))

    def is_valid(self):
        res = self.session.get(routes.login()).content
        alert = parser.find(res, ["div", {"class": "alert-danger"}])
        return False if (not alert) else "already" in alert.text

    def authenticate(self, email, password):
        res = self.session.get(routes.ROOT).content
        auth_token = parser.select(res, "meta[name=csrf-token]")[0].get("content")
        formdata = {
            "authenticity_token": auth_token,
            "user[email]" : email,
            "user[password]": password,
            "user[remember_me]": 1
        }
        req = self.session.post(routes.login(), data=formdata)
        with open(Session.DEFAULT_COOKIES_FILE, "wb") as file:
            pickle.dump(self.session.cookies, file)
        return True

    def get(self, url):
        if (self.is_valid()):
            return self.session.get(url).content
        else:
            raise Exception("Session expired. Please re-login")

    def post(self, url, data):
        if (self.is_valid()):
            return self.session.post(url, data=data).content
        else:
            raise Exception("Session expired. Please re-login")
