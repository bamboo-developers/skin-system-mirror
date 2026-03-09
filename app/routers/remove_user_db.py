from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import skin_system

router = APIRouter()

@router.get('/sys/remove/user/{username}')
@skin_system.token_required(1, 'GET')
def func(username: str, request: Request):
    if not skin_system.DB.record_exists('user_data', 'nickname', username):
        return JSONResponse({'message': 'nickname not found', 'code': 404}, status_code=404)
    if skin_system.DB.remove_row('user_data', nickname=username):
        return JSONResponse({'message': 'success', 'code': 200}, status_code=200)
    return JSONResponse({'message': 'something went wrong', 'code': 500}, status_code=500)
