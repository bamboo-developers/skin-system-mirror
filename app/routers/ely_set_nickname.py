from flask import Blueprint, request, jsonify
import skin_system

bp = Blueprint('add_nickname_db', __name__)

@bp.route('/ely/set/<username>')
@skin_system.token_required(1)
def func(username):
    redirect_nickname = request.args.get('redirect')

    if not redirect_nickname:
        return jsonify({'message': 'parameter "redirect" is required', 'code': 400}), 400

    if redirect_nickname == '<del>':
        if not skin_system.valid_minecraft_nick(username):
            return jsonify({'message': f'invalid nickname: {username}', 'code': 422}), 422
    else:
        for nick in [username, redirect_nickname]:
            if not skin_system.valid_minecraft_nick(nick):
                return jsonify({'message': f'invalid nickname: {nick}', 'code': 422}), 422

    result = skin_system.DB.set_nickname_ely(username, redirect_nickname)

    if result:
        return jsonify({'message': 'success', 'code': 200}), 200
    else:
        return jsonify({'message': 'redirect nickname already exists', 'code': 400}), 400
