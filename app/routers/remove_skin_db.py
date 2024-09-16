from flask import Blueprint, request, jsonify
import skin_system

bp = Blueprint('remove_skin_db', __name__)

@bp.route('/sys/remove/skin/<id>')
@skin_system.token_required(1, 'GET')
def func(id):
    if not skin_system.DB.record_exists('skin_data', 'id', id):
        return jsonify({'message': 'skin not found', 'code': 404}), 404

    if skin_system.DB.remove_row('skin_data', skin_id=id):
        return jsonify({'message': 'success', 'code': 200}), 200

    return jsonify({'message': 'something went wrong', 'code': 500}), 500
