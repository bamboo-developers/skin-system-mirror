import uuid
from flask import request, jsonify
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import subprocess
from skin_system import get_path, convert_skin
import os
from PIL import Image

UPLOAD_FOLDER = get_path('temp/', "..")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DEFAULT_STORAGE_TIME = 120

def     temp_skin_storge(file, web=True, time=120):
    if not file:
        return jsonify({'message': 'No file provided', 'code': 400}), 400

    if isinstance(file, str):
        try:
            image = Image.open(file)
        except Exception as e:
            return f"Error opening file: {str(e)}"
    else:
        try:
            file.seek(0)
            image = Image.open(file)
        except Exception as e:
            return f"Error processing image: {str(e)}"

    if image.size not in [(64, 64), (64, 32)]:
        return jsonify({'message': 'It seems not to be a valid Minecraft skin', 'code': 400}), 400

    if image.size == (64, 32):
        image = convert_skin(image)

    filename = secure_filename(f"{uuid.uuid4()}_{os.path.basename(file if isinstance(file, str) else file.filename)}")
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    image.save(file_path)

    subprocess.Popen(f'sh -c "sleep {time} && rm -f {file_path}"', shell=True)

    if web:
        storage_time = int(request.form.get('time', DEFAULT_STORAGE_TIME))
        download_url = request.host_url + 'temp/get/' + filename
        deletion_time = datetime.now() + timedelta(seconds=storage_time)

        return jsonify({'download_url': download_url, 'expires_at': deletion_time.isoformat()})

    return file_path