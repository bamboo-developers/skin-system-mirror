from fastapi import APIRouter, Request
from fastapi.responses import Response
import skin_system

router = APIRouter()

@router.get('/profile/{username}')
@skin_system.token_required(0)
def func(username: str, request: Request, unsigned: str = 'true'):
    username = skin_system.DB.what_redirect_of(username, 'ely')
    url = f"http://skinsystem.ely.by/profile/{username['ely']}?unsigned={unsigned}"
    return skin_system.resolve(url)
