from fastapi import APIRouter, Request
import skin_system

router = APIRouter()

@router.get('/textures/{username}')
@skin_system.token_required(0)
def func(username: str, request: Request):
    username = skin_system.DB.what_redirect_of(username, 'ely')
    url = f"http://skinsystem.ely.by/textures/{username['ely']}"
    return skin_system.resolve(url)
