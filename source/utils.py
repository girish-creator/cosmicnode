import requests
import json


def get_access_token():
    try:
        login_url = "http://52.59.232.190/api/v1/login"
        login_payload = json.dumps({
            "email": "sd.cosmicnode@gmail.com", "password": "password"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", login_url, headers=headers, data=login_payload)
        access_token = {"accessToken": response.json()["data"]["accessToken"]}
        headers.update(access_token)
        return headers

    except Exception as error:
        raise error
