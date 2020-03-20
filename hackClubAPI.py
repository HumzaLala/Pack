import requests, json

class APIException(Exception):
    pass

class HackClubAPI:
    
    # Remove default in prod
    def __init__(self, apiRoot):
        self.apiRoot = apiRoot
    
    def makeRequest(self, username, email):
        userDataDict =  {
            "username": username,
            "email": email
        }
        r = requests.post(self.apiRoot, data=userDataDict)
        try:
            rJson = r.json()
        except:
            raise ValueError("Response was not JSON")

        if rJson["status"] == "success":
            return r
        else:
            raise APIException("API did not return OK")