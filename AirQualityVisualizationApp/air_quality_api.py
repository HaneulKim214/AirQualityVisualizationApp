import os
import requests

def get_aqi(city):
    beijing_api = os.environ.get('AQI_api_key')
    url = f'https://api.waqi.info/feed/{city}/?token={beijing_api}'
    try:
        response = requests.get(url).json()
        if response['status'] == 'ok':
            # aqi data if api call successful
            return response
        else: # case where call is successful but error status
            return None
    except:
        return None


def clean_json(city):
    """
    for given city depending on success of api call returns boolean object
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