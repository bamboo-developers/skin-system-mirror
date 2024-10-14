from flask import Blueprint, jsonify
import skin_system

bp = Blueprint('remove_user_db', __name__)

@bp.route('/sys/remove/user/<username>')
@skin_system.token_required(1, 'GET')
def func(username):
    if not skin_system.DB.record_exists('user_data', 'nickname', username):
        return jsonify({'message': 'nickname not found', 'code': 404}), 404

    if skin_system.DB.remove_row('user_data', nickname=username):
        return jsonify({'message': 'success', 'code': 200}), 200

    return jsonify({'message': 'something went wrong', 'code': 500}), 500
