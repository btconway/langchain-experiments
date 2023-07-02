import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Set Slack API credentials
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_BOT_USER_ID = os.getenv("SLACK_BOT_USER_ID")

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    handlers=[logging.StreamHandler()])

def get_bot_user_id():
    """
    Get the bot user ID using the Slack API.
    Returns:
        str: The bot user ID.
    """
    try:
        # Initialize the Slack client with your bot token
        slack_client = WebClient(token=SLACK_BOT_TOKEN)
        response = slack_client.auth_test()
        bot_user_id = response["user_id"]
        logging.info(f"Retrieved bot user ID: {bot_user_id}")
        return bot_user_id
    except SlackApiError as e:
        logging.error(f"Slack API error occurred: {e.response['error']}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

# Test the function
get_bot_user_id()
