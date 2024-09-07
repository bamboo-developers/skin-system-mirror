from flask import Blueprint, jsonify
import skin_system

bp = Blueprint('search_on_db', __name__)

@bp.route('/db/search/<username>')
@skin_system.token_required(1)
def func(username):
    if username != "<all>":
        for nick in [username]:
            if not skin_system.valid_minecraft_nick(nick):
                return jsonify({'message': f'invalid nickname: {nick}'}), 403
    else: pass

    return skin_system.search_on_db(username)
