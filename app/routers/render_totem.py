from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response
from io import BytesIO
import skin_system

router = APIRouter()

@router.get('/render/totem/{username}')
@skin_system.token_required(0)
def func(username: str, request: Request, round_head: bool = True):
    try:
        username = skin_system.DB.what_redirect_of(username, 'ely')
        url = f"http://skinsystem.ely.by/skins/{username['ely']}.png"
        skin_image = skin_system.resolv_skin(url)

        processed_totem = skin_system.process_totem(skin_image, round_head)

        img_io = BytesIO()
        processed_totem.save(img_io, 'PNG')
        img_io.seek(0)

        return Response(content=img_io.read(), media_type='image/png')
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    