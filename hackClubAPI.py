import requests, json

# Custom exception used when HC API returns non-200
class APIException(Exception):
    pass

# Primary API Class
class HackClubAPI:

    # Define API route
    def __init__(self, apiRoot):
        self.apiRoot = apiRoot

    def makeRequest(self, username, email):
        # Dictionary assembly for submission
        userDataDict = {"username": username, "email": email}

        # Making the request
        r = requests.post(self.apiRoot, data=userDataDict)

        # Attempting to interpret the JSON
        try:
            rJson = r.json()
        except:
            raise ValueError("Response was not JSON")

        # Very easy way to return sucess from the function
        if rJson["status"] == "success":
            return r
        else:
            raise APIException("API did not return OK")
