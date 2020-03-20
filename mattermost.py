# Standard Libaries
import http.client, json

# serverUrl should be just the subdomain/domain
# eg, "chat.srnd.org"
# webHookKey should be the key trailing /hooks/

class Mattermost:
    def __init__(self, serverUrl, webHookKey):
        self.serverUrl = serverUrl
        self.key = webHookKey

    def _postMMWebhook(self, payload):
        conn = http.client.HTTPSConnection(self.serverUrl)

        headers = {"content-type": "application/json", "cache-control": "no-cache"}

        conn.request("POST", f"/hooks/{self.key}", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    def postToChannel(self, channel, text):
        payload = {"text": text, "channel": channel}
        return self._postMMWebhook(json.dumps(payload))