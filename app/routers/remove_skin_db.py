from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import skin_system

router = APIRouter()

@router.get('/sys/remove/skin/{id}')
@skin_system.token_required(1, 'GET')
def func(id: str, request: Request):
    if not skin_system.DB.record_exists('skin_data', 'id', id):
        return JSONResponse({'message': 'skin not found', 'code': 404}, status_code=404)
    if skin_system.DB.remove_row('skin_data', skin_id=id):
        return JSONResponse({'message': 'success', 'code': 200}, status_code=200)
    return JSONResponse({'message': 'something went wrong', 'code': 500}, status_code=500)
