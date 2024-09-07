from flask import Blueprint, request
import skin_system

bp = Blueprint('signed_textures', __name__)

@bp.route('/textures/signed/<username>')
@skin_system.token_required(0)
def func(username):
    username = skin_system.what_redirect_of(username)

    url = f"http://skinsystem.ely.by/textures/signed/{username}"

    proxy = request.args.get('proxy', default='false', type=str)

    url = f"{url}?proxy={proxy}"

    return skin_system.resolve(url)