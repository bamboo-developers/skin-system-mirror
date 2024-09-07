from flask import Blueprint, request, jsonify
import skin_system

bp = Blueprint('add_nickname_db', __name__)

@bp.route('/db/add/<username>')
@skin_system.token_required(1)
def func(username):
    redirect_nickname = request.args.get('redirect')

    if not redirect_nickname:
        return jsonify({'message': 'parameter "redirect" is required'}), 403


    for nick in [username, redirect_nickname]:
        if not skin_system.valid_minecraft_nick(nick):
            return jsonify({'message': f'invalid nickname: {nick}'}), 403


    return skin_system.add_nickname(username, redirect_nickname)
