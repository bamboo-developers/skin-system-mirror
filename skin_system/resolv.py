import requests
from flask import Response


def resolve(url):
    response = requests.get(url)

    return Response(response.content, content_type=response.headers['Content-Type'])
