from flask import Blueprint, request, jsonify
import skin_system

bp = Blueprint('delete_nickname_db', __name__)

@bp.route('/db/remove/<username>')
@skin_system.token_required(1)
def func(username):
    for nick in [username]:
        if not skin_system.valid_minecraft_nick(nick):
            return jsonify({'message': f'invalid nickname: {nick}', 'code': 422}), 422

    return skin_system.remove_nickname(username)
