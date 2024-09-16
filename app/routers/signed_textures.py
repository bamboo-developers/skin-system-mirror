from flask import Blueprint, jsonify, request
import skin_system

bp = Blueprint('signed_textures', __name__)

@bp.route('/textures/signed/<username>')
@skin_system.token_required(0)
def func(username):
    proxy = request.args.get('proxy', default='false', type=str)

    what_skin_system = skin_system.DB.what_redirect_of(username)
    print(what_skin_system)

    if 'ely' in what_skin_system:
        username = what_skin_system['ely']
        print(username)

        url = f"http://skinsystem.ely.by/textures/signed/{username}?proxy={proxy}"

        return skin_system.resolve(url)

    else:
        data = skin_system.DB.return_data_for_system(nickname=username)
        return jsonify(data), 200