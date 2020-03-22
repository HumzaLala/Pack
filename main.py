from hackClubAPI import HackClubAPI
from github import Github
from os import environ
from flask import Flask, jsonify, request
from mattermost import Mattermost

# Constants
app = Flask(__name__)
ghAPI = Github(environ["GHKEY"])
hcAPI = HackClubAPI(environ["HCURL"])
mattermostSession = Mattermost("chat.srnd.org", environ["MMKEY"])


def submitApplication(username, email):
    try:
        username = ghAPI.get_repo("srnd/Pack").get_issue(number=int(id)).user.login
        email = ghAPI.get_repo("srnd/Pack").get_issue(number=int(id)).body
        application = hcAPI.makeRequest(username=username, email=email)
        return True
    except:
        return False


@app.route("/")
def index():
    return jsonify({"status": 200})


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST" and request.is_json == True:
        data = request.json
        if (
            data["action"] == "labeled"
            and data["issue"]["labels"][0]["name"] == "Approved"
        ):
            print("Capture")
            try:
                application = hcAPI.makeRequest(
                    username=data["issue"]["user"]["login"], email=data["issue"]["body"]
                )
            except:
                mattermostSession.postToChannel(
                    "codecup-notifs", f"Submission failure ```json{data}```"
                )
                return jsonify({"action": "none", "error": "failed hcAPI"})

            return jsonify({"action": "Submitted"})
        else:
            return jsonify({"action": "none"})


if __name__ == "__main__":
    app.run(host="0.0.0.0:8000", debug=True)
