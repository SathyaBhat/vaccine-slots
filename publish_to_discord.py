from os import environ
import requests
from datetime import datetime
from pytz import timezone

now_time = datetime.now(timezone('Asia/Kolkata'))

def publish_message(slots_info):
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