from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response
from io import BytesIO
import skin_system

y_allowed = ["front", "back"]
z_allowed = ["up", "down"]

router = APIRouter()

@router.get('/perspective/{username}')
@skin_system.token_required(0)
def func(username: str, request: Request, scale: int = 8, y: str = 'front', z: str = 'up'):
    username = skin_system.DB.what_redirect_of(username, 'ely')
    url = f"http://skinsystem.ely.by/skins/{username['ely']}.png"
    skin_image = skin_system.resolv_skin(url)

    if skin_image is None:
        return JSONResponse({'message': 'skin not found', 'code': 404}, status_code=404)

    scale = min(scale, 100)

    if y not in y_allowed or z not in z_allowed:
        return JSONResponse({"message": "Invalid parameters", "code": 400}, status_code=400)

    processed_skin = skin_system.perspective(skin_image, scale, y, z)
    img_io = BytesIO()
    processed_skin.save(img_io, 'PNG')
    img_io.seek(0)

    return Response(content=img_io.read(), media_type='image/png')
