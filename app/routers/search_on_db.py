from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import skin_system

router = APIRouter()

@router.get('/sys/search/{args}')
@skin_system.token_required(1)
def func(args: str, request: Request, table: str = None):
    if not table:
        return JSONResponse({'message': 'parameter "table" is required', 'code': 400}, status_code=400)
    if table not in ('user_data', 'skin_data'):
        return JSONResponse({'message': f'invalid table: {table}', 'code': 422}, status_code=422)

    if args != "<all>":
        if not skin_system.valid_minecraft_nick(args):
            return JSONResponse({'message': f'invalid nickname: {args}', 'code': 422}, status_code=422)

    if table == 'skin_data':
        return skin_system.DB.view_on_db('skin_data', skin_id=args)
    return skin_system.DB.view_on_db('user_data', nickname=args, user_id=args)
