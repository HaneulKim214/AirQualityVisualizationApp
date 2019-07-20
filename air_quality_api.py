import os
import requests

def get_aqi(city):
    beijing_api = os.environ.get('AQI_api_key')
    url = f'https://api.waqi.info/feed/{city}/?token={beijing_api}'
    try:
        response = requests.get(url).json()
        if response['status'] == 'ok':
            # aqi data if api call successful
            return response["data"]["aqi"]
            aqi_list.append(response["data"]["aqi"])
        else: # call is successful however can get error status
            return None
    except:
        return None


def clean_json(city):
    """
    This function grabs city and return boolean object appropriately
    """
    beijing_api = os.environ.get('AQI_api_key')
    url = f'https://api.waqi.info/feed/{city}/?token={beijing_api}'
    try:
        response = requests.get(url).json()
        if response["status"] == 'ok':
            return True
        else:
            return False
    # if some kind of error when calling api
    except:
        return False