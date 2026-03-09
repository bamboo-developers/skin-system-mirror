from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import skin_system

router = APIRouter()

@router.get('/sys/toggle/redirect/{username}')
@skin_system.token_required(1)
def func(username: str, request: Request, toggle: str = None):
    if not toggle:
        return JSONResponse({'message': 'parameter "toggle" is required', 'code': 400}, status_code=400)
    if not skin_system.valid_minecraft_nick(username):
        return JSONResponse({'message': f'invalid nickname: {username}', 'code': 422}, status_code=422)

    result = skin_system.DB.toggle_redirect(username, toggle)
    if result:
        return JSONResponse({'message': 'success', 'code': 200}, status_code=200)
    return JSONResponse({'message': 'something went wrong', 'code': 500, 'error': result}, status_code=500)
