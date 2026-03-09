from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
import skin_system
import os

'''
curl -X POST http://127.0.0.1:5000/temp \
  -F 'file=@/path/to/your/skin.png' \
  -F 'token=token' \
  -F 'time=60'
'''

router = APIRouter()

UPLOAD_FOLDER = skin_system.get_path('temp/', "..")

@router.post('/temp')
@skin_system.token_required(1, method='POST')
async def upload_skin(
    request: Request,
    file: UploadFile = File(None),
    time: int = Form(120)
):
    time = min(time, 300)

    if not file:
        return JSONResponse({'message': 'No file provided', 'code': 400}, status_code=400)

    result = skin_system.temp_skin_storge(file, web=True, time=time)
    if isinstance(result, tuple):
        return result
    return result

@router.get('/temp/get/{filename}')
def download_skin(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')
