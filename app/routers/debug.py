import datetime
import os
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()
start_time = datetime.datetime.now(datetime.timezone.utc)

def get_uptime():
    return str(datetime.datetime.now(datetime.timezone.utc) - start_time).split('.')[0]

@router.get('/debug')
def index(request: Request):
    return JSONResponse({
        'message': f'{os.environ.get("SKIN_SYSTEM_NAME")} online and ready to work :-)',
        'code': 200,
        'uptime': get_uptime(),
        "requester's IP": request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
    })