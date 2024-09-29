from flask import Blueprint
import skin_system

bp = Blueprint('textures', __name__)

@bp.route('/textures/<username>')
@skin_system.token_required(0)
def func(username):
    username = skin_system.DB.what_redirect_of(username, 'ely')

    url = f"http://skinsystem.ely.by/textures/{username['ely']}"

    return skin_system.resolve(url)