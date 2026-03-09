import requests
from fastapi.responses import Response

def resolve(url):
    response = requests.get(url)
    if response.status_code != 200:
        return Response(content=b'', status_code=404)
    return Response(content=response.content, media_type=response.headers['Content-Type'])
