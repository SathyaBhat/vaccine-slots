from os import environ
import requests
from datetime import datetime
from pytz import timezone
from os import getenv
import requests
import sys

now_time = datetime.now(timezone('Asia/Kolkata'))

def publish_failure(message):
    discord_webhook = environ.get('DISCORD_FAILURE_WEBHOOK')
    content_text = "general bot failure {message}"
    discord_message = {
        "content": f"{content_text}"
    }
    discord_response = requests.post(url=discord_webhook, data=discord_message)

def publish_to_discord(slots_info):
    discord_webhook = environ.get('DISCORD_WEBHOOK')
    content_text = "\n".join(slots_info)
    discord_message = {
        "content": f"Vaccination slots info as of {now_time.strftime('%I:%M:%S %p')} IST: \n {content_text}",
        # "embeds": [
        #     {
        #         "title": "Vaccination Slots info",
        #         "description": f"{slots_info}",
        #         "type": "rich",
        #         "color": 4289797
        #     }
        # ]
    }

    print(discord_webhook)
    print(discord_message)
    discord_response = requests.post(url=discord_webhook, data=discord_message)
    if discord_response.status_code != 204:
        print(f"Could not post to discord, status code {discord_response.status_code} {discord_response.text}")
        publish_failure(f"Could not post to discord, status code {discord_response.status_code} {discord_response.text}")

def publish_to_telegram(slots_info):
    telegram_api_token = getenv('TELEGRAM_API_TOKEN', None)
    telegram_channel_id = getenv('TELEGRAM_CHANNEL_ID', None)
    content_text = " ".join(slots_info)[0:4095]
    telegram_api_url = f"https://api.telegram.org/bot{telegram_api_token}/sendMessage"
    payload = {'chat_id':telegram_channel_id, 'text':content_text}
    response = requests.get(telegram_api_url, params=payload)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Message dispatch failed with error {response.status_code} {response.text}")
        publish_failure(f"Message dispatch failed with error {response.status_code} {response.text}")

def publish_message(slots_info):
    try:
        publish_to_discord(slots_info)
        telegram_enabled = getenv('TELEGRAM_ENABLED', 'NO')
        if telegram_enabled == 'YES':
            publish_to_telegram(slots_info)
    except:
        error = f"Unexpected error: {sys.exc_info()[0]}" 
        print(error)
        publish_failure(error)