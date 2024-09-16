from flask import Blueprint, jsonify, request
import skin_system

bp = Blueprint('toggle_redirect', __name__)

@bp.route('/sys/toggle/redirect/<username>')
@skin_system.token_required(1)
def func(username):
    toggle = request.args.get('toggle')
    if not toggle:
        return jsonify({'message': 'parameter "toggle" is required', 'code': 400}), 400

    if not skin_system.valid_minecraft_nick(username):
        return jsonify({'message': f'invalid nickname: {username}', 'code': 422}), 422

    result = skin_system.DB.toggle_redirect(username, toggle)

    if result:
        return jsonify({'message': 'success', 'code': 200}), 200
    else:
        return jsonify({'message': 'something went wrong', 'code': 500, 'error': result}), 500