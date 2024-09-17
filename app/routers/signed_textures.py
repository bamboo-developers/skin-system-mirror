from flask import Blueprint, jsonify, request
import skin_system

bp = Blueprint('signed_textures', __name__)

@bp.route('/textures/signed/<username>')
@skin_system.token_required(0)
def func(username):
    proxy = request.args.get('proxy', default='false', type=str)
    if proxy != 'true':
        proxy = False
    else: proxy = True

    what_skin_system = skin_system.DB.what_redirect_of(username)

    if 'ely' in what_skin_system:
        username = what_skin_system['ely']

        url = f"http://skinsystem.ely.by/textures/signed/{username}?proxy={proxy}"

        return skin_system.resolve(url)

    else:
        data = skin_system.DB.return_texture_data_for_system(nickname=username, proxy=proxy)
        return jsonify(data), 200