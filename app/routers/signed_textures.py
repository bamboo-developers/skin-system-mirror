from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import skin_system

router = APIRouter()

@router.get('/textures/signed/{username}')
@skin_system.token_required(0)
def func(username: str, request: Request, proxy: str = 'false'):
    proxy_bool = proxy == 'true'

    what_skin_system = skin_system.DB.what_redirect_of(username)
    if 'ely' in what_skin_system:
        username = what_skin_system['ely']
        url = f"http://skinsystem.ely.by/textures/signed/{username}?proxy={proxy_bool}"
        return skin_system.resolve(url)
    else:
        data = skin_system.DB.return_texture_data_for_system(nickname=username, proxy=proxy_bool)
        return JSONResponse(data, status_code=200)
    