from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
import skin_system
import os

'''
curl -X POST http://127.0.0.1:5000/sys/add/user \
  -F 'file=@/path/to/your/skin.png' \
  -F 'nickname=yiski'
  -F 'redirect=0'
  -F 'token=token'
'''

router = APIRouter()

@router.post('/sys/add/user')
@skin_system.token_required(1, method='POST')
async def upload_skin(
    request: Request,
    file: UploadFile = File(None),
    nickname: str = Form(None),
    redirect: int = Form(0)
):
    redirect_ely = min(redirect, 1)

    if not file:
        return JSONResponse({'message': 'No file provided', 'code': 400}, status_code=400)
    if not nickname:
        return JSONResponse({'message': 'No nickname provided', 'code': 400}, status_code=400)
    if not skin_system.valid_minecraft_nick(nickname):
        return JSONResponse({'message': f'invalid nickname: {nickname}', 'code': 422}, status_code=422)

    file_path = os.path.join('/tmp', file.filename)
    with open(file_path, 'wb') as f:
        f.write(await file.read())

    try:
        skin_id = skin_system.DB.get_sign_skin(nickname, file_path)
        skin_system.DB.toggle_redirect(nickname, redirect_ely)
        result = skin_system.DB.set_skin_id(nickname, skin_id)

        if not result:
            return JSONResponse({'message': 'something went wrong', 'code': 500, 'error': result}, status_code=500)
        if isinstance(result, tuple):
            return result
        return JSONResponse({'message': 'success', 'code': 200}, status_code=200)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            