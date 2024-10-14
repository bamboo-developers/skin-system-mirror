from flask import Flask
from werkzeug.exceptions import HTTPException
import skin_system
from skin_system.manage_db import create_db
from .extensions import limiter
from .routers import (skin, render, perspective_render, errors, textures, profile, signature_ver_key, signed_textures,
                      ely_set_nickname, remove_skin_db, search_on_db, debug, temp_save_skins, sign_skin, toggle_redirect, remove_user_db)


def create_app():
    app = Flask(__name__)

    limiter.init_app(app)

    app.register_error_handler(HTTPException, errors.handle_error)

    app.register_blueprint(debug.bp)
    app.register_blueprint(skin.bp)
    app.register_blueprint(render.bp)
    app.register_blueprint(perspective_render.bp)
    app.register_blueprint(textures.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(signature_ver_key.bp), app.register_blueprint(signature_ver_key.bp2)
    app.register_blueprint(signed_textures.bp)
    app.register_blueprint(ely_set_nickname.bp)
    app.register_blueprint(remove_skin_db.bp)
    app.register_blueprint(search_on_db.bp)
    app.register_blueprint(temp_save_skins.bp)
    app.register_blueprint(sign_skin.bp)
    app.register_blueprint(toggle_redirect.bp)
    app.register_blueprint(remove_user_db.bp)

    create_db()
    skin_system.load_tokens()

    return app
