import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App as SlackApp  # Rename the import here
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
from functions import chat_interactive  # Import the function here

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

# Initialize the Slack app
slack_app = SlackApp(token=SLACK_BOT_TOKEN)  # Rename the Slack app here

# Initialize the Flask app
# Flask is a web application framework written in Python
app = Flask(__name__)  # Rename the Flask app here
handler = SlackRequestHandler(slack_app)  # Use the renamed Slack app here

@slack_app.event("app_mention")  # Use the renamed Slack app here
def handle_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    text = body["event"]["text"]

    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()

    say("Sure, I'll get right on that!")
    response = chat_interactive(text)  # Call the function here
    say(response)

@app.route("/slack/events", methods=["POST"])  # Use the renamed Flask app here
def slack_events():
    """
    Route for handling Slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    return handler.handle(request)

# Run the Flask app
if __name__ == "__main__":
    app.run()  # Use the renamed Flask app here
