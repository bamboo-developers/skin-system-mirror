from fastapi import FastAPI
from fastapi.exceptions import HTTPException
import skin_system
from skin_system.manage_db import create_db
from .extensions import limiter
from .routers import (skin, render, render_totem, perspective_render, errors, textures, profile, signature_ver_key, signed_textures,
                      ely_set_nickname, remove_skin_db, search_on_db, debug, temp_save_skins, sign_skin, toggle_redirect, remove_user_db)

def create_app() -> FastAPI:
    app = FastAPI()

    app.state.limiter = limiter
    app.add_exception_handler(Exception, errors.handle_error)
    app.add_exception_handler(HTTPException, errors.handle_error)

    app.include_router(debug.router)
    app.include_router(skin.router)
    app.include_router(render.router)
    app.include_router(render_totem.router)
    app.include_router(perspective_render.router)
    app.include_router(textures.router)
    app.include_router(profile.router)
    app.include_router(signature_ver_key.router)
    app.include_router(signature_ver_key.router2)
    app.include_router(signed_textures.router)
    app.include_router(ely_set_nickname.router)
    app.include_router(remove_skin_db.router)
    app.include_router(search_on_db.router)
    app.include_router(temp_save_skins.router)
    app.include_router(sign_skin.router)
    app.include_router(toggle_redirect.router)
    app.include_router(remove_user_db.router)

    @app.on_event("startup")
    async def startup_event():
        create_db()
        skin_system.load_tokens()

    return app
