from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
import skin_system

router = APIRouter()

@router.get('/ely/set/{username}')
@skin_system.token_required(1)
def func(username: str, request: Request, redirect: str = None):
    if not redirect:
        return JSONResponse({'message': 'parameter "redirect" is required', 'code': 400}, status_code=400)

    if redirect == '<del>':
        if not skin_system.valid_minecraft_nick(username):
            return JSONResponse({'message': f'invalid nickname: {username}', 'code': 422}, status_code=422)
    else:
        for nick in [username, redirect]:
            if not skin_system.valid_minecraft_nick(nick):
                return JSONResponse({'message': f'invalid nickname: {nick}', 'code': 422}, status_code=422)

    result = skin_system.DB.set_redirected_nickname_ely(username, redirect)
    if result:
        return JSONResponse({'message': 'success', 'code': 200}, status_code=200)
    else:
        return JSONResponse({'message': 'redirect nickname already exists', 'code': 400}, status_code=400)