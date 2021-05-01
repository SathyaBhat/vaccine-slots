import sys
import json
import requests
from datetime import datetime
from os import getenv
from publish_to_discord import publish_message

def get_slots_info():
    current_date = datetime.today().strftime("%d-%m-%y")
    district_id = getenv('DISTRICT_ID', 000) # This is Bangalore / BBMP
    if len(sys.argv) > 1:
        district_id = int(sys.argv[1])

    print(f"Looking for vaccination availability in district ID {district_id}")

    # Replace the above with your favourite district:
    #
    # First, find your state ID:
    # $ curl -X GET "https://api.demo.co-vin.in/api/v2/admin/location/states" -H "accept: application/json" -H "Accept-Language: en_IN"| python -m json.tool
    #
    # Then find your district ID (replace state ID "21" below with your state ID):
    # $ curl -X GET "https://cdn-api.co-vin.in/api/v2/admin/location/districts/21" -H "accept: application/json" -H "Accept-Language: en_IN"| python -m json.tool

    CALENDAR_ENDPOINT = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={current_date}"

    response = requests.get(
            CALENDAR_ENDPOINT,
            headers={
                'Accept': 'application/json',
                'Accept-Language': 'en_IN'},
            )
    if response.status_code != 200:
        print(f"Something went wrong when fetching {CALENDAR_ENDPOINT}. Response below:")
        print(response.status_code)
        print(response.text)
        exit()

    centers = response.json()['centers']
    eligible_available_centers = []
    SHOW_EMPTY_SLOTS = getenv('SHOW_EMPTY_SLOTS', False)
    print(SHOW_EMPTY_SLOTS)
    for center in centers:
        for session in center['sessions']:
            if session['min_age_limit'] != 45:
                if SHOW_EMPTY_SLOTS or session['available_capacity'] > 0:
                    eligible_available_centers.append((center, session))

    if len(eligible_available_centers) == 0:
        print("Sorry, no available centers yet. Stay home")
    else:
        for center, session in eligible_available_centers:
            info_text = []
            info_text.append(f"{center['pincode']}: {session['available_capacity']} slots available at {center['name']}")
        publish_message(info_text)
    return

if __name__ == "__main__":
    get_slots_info()