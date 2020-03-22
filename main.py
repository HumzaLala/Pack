from hackClubAPI import HackClubAPI, APIException
from github import Github
from os import environ
from flask import Flask, jsonify, request
from mattermost import Mattermost

# Constants
app = Flask(__name__)
ghAPI = Github(environ["GHKEY"])
hcAPI = HackClubAPI(environ["HCURL"])
mattermostSession = Mattermost("chat.srnd.org", environ["MMKEY"])


# Root route, used by Stackdriver ping
@app.route("/")
def index():
    return jsonify({"status": 200})


# Webhook route used by GitHub
@app.route("/submit", methods=["POST"])
def submit():

    # Verify that request is formated correctly
    if request.method == "POST" and request.is_json == True:
        data = request.json

        # Checks POST data if action is applying a label and is the 'Approved' label
        if (
            data["action"] == "labeled"
            and data["issue"]["labels"][0]["name"] == "Approved"
        ):
            # Used for Stackdriver monitoring, as a fallback
            print(f"Capture {data['issue']['user']['login']} {data['issue']['body']}")

            # Attempting to make call to Hack Club
            try:
                application = hcAPI.makeRequest(
                    username=data["issue"]["user"]["login"], email=data["issue"]["body"]
                )
            except APIException:

                # Send POST data to mattermost in case of error
                mattermostSession.postToChannel(
                    "codecup-notifs", f"Submission failure ```json{data}```"
                )

                # JSON data isn't used for anything on the GH side, could be useful in the future
                return jsonify({"action": "none", "error": "failed hcAPI"})

            except ValueError as error:

                # Send POST data to mattermost in case of error
                mattermostSession.postToChannel(
                    "codecup-notifs", f"Interpetation error: {error} ```json{data}```"
                )

                # JSON data isn't used for anything on the GH side, could be useful in the future
                return jsonify({"action": "none", "error": "failed JSON Parsing"})

            return jsonify({"action": "Submitted"})
        else:

            # Sent when any other action is sent or wrong label
            return jsonify({"action": "none"})


if __name__ == "__main__":
    app.run(host="0.0.0.0:8000", debug=True)
