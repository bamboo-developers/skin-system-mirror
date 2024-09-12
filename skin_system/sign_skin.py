import requests
import json
from flask import jsonify
import os

def sign_skin(name):
    url = 'https://api.mineskin.org/generate/url'

    headers = {
        'accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36',
        'Authorization': f'{os.environ.get("SIGN_API_TOKEN")}',
        'Content-Type': 'application/json'
    }

    data = {
        'url': 'https://skin-api.bambooland.fun/skin/yiski?token=token1',
        'visibility': 1,
        'name': f'{name}'
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()

        result = {
            'name': response_json.get('name', ''),
            'value': response_json.get('data', {}).get('texture', {}).get('value', ''),
            'signature': response_json.get('data', {}).get('texture', {}).get('signature', ''),
            'timestamp': response_json.get('timestamp', ''),
            'skin_url': response_json.get('data', {}).get('texture', {}).get('url', '')
        }

        return json.dumps(result, indent=4)

    else:
        return jsonify({"message": "failed",
                        "code": response.status_code,
                        "response text": response.text
                        }), response.status_code