from flask import Blueprint
import skin_system

bp = Blueprint('textures', __name__)

@bp.route('/textures/<username>')
@skin_system.token_required(0)
def func(username):
    username = skin_system.what_redirect_of(username)

    url = f"http://skinsystem.ely.by/textures/{username}.png"

    return skin_system.resolve(url)