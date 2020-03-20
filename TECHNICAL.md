# Setting up the bot

Needed ENV:
 - HCURL (URL for Hack Club endpoint)
 - GHAPI (Access Token for GitHub)
 - MMKEY (Mattermost Key)

How to run:
 - Define ENV
 - Run the WSGI stack however you'd like (`main:app`)
 - Set webhook in GitHub
 - ???
 - Done

How to use:
 - In issues, mark issues that are Approved with the `Approved` label
 - Wait a few seconds for the webhook
 - Close the issue if you'd like (or not, I'm not the boss of you)