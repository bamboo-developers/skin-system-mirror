import requests
from flask import Response


def resolve(url):
    response = requests.get(url)

    if response.status_code != 200:
        return {}, 404

    return Response(response.content, content_type=response.headers['Content-Type'])
