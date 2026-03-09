import uuid
from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from starlette.datastructures import UploadFile
import subprocess
from skin_system import get_path, convert_skin
import os
from PIL import Image

UPLOAD_FOLDER = get_path('temp/', "..")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DEFAULT_STORAGE_TIME = 120

def temp_skin_storge(file, web=True, time=120, request: Request = None):
    if not file:
        return JSONResponse({'message': 'No file provided', 'code': 400}, status_code=400)

    if isinstance(file, str):
        try:
            image = Image.open(file)
        except Exception as e:
            return f"Error opening file: {str(e)}"
    else:
        try:
            if isinstance(file, UploadFile):
                file.file.seek(0)
                image = Image.open(file.file)
            else:
                file.seek(0)
                image = Image.open(file)
        except Exception as e:
            return f"Error processing image: {str(e)}"

    if image.size not in [(64, 64), (64, 32)]:
        return JSONResponse({'message': 'It seems not to be a valid Minecraft skin', 'code': 400}, status_code=400)

    if image.size == (64, 32):
        image = convert_skin(image)

    filename = f"{uuid.uuid4()}_{os.path.basename(file if isinstance(file, str) else file.filename)}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    image.save(file_path)

    subprocess.Popen(f'sh -c "sleep {time} && rm -f {file_path}"', shell=True)

    if web and request:
        download_url = str(request.base_url) + 'temp/get/' + filename
        deletion_time = datetime.now() + timedelta(seconds=time)
        return JSONResponse({'download_url': download_url, 'expires_at': deletion_time.isoformat()})

    return file_path
