from flask import Blueprint, request, jsonify
import skin_system
import os

'''
curl -X POST http://127.0.0.1:5000/sys/add/user \
  -F 'file=@/path/to/your/skin.png' \
  -F 'nickname=yiski'
  -F 'redirect=0'
  -F 'token=token'
'''

bp = Blueprint('sign_skin', __name__)


@bp.route('/sys/add/user', methods=['POST'])
@skin_system.token_required(1, method='POST')
def upload_skin():
    file = request.files.get('file')
    nickname = request.form.get('nickname')
    redirect_ely: int = min(request.form.get('redirect', default=0, type=int), 1)

    if not file:
        return jsonify({'message': 'No file provided', 'code': 400}), 400
    if not nickname:
        return jsonify({'message': 'No nickname provided', 'code': 400}), 400
    if not skin_system.valid_minecraft_nick(nickname):
        return jsonify({'message': f'invalid nickname: {nickname}', 'code': 422}), 422

    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    try:
        skin_id = skin_system.DB.write_sign_skin(file_path)
        skin_system.DB.toggle_redirect(nickname, redirect_ely)
        result = skin_system.DB.set_skin_id(nickname, skin_id)

        if not result:
            return jsonify({'message': 'something went wrong', 'code': 500, 'error': result}), 500

        if isinstance(result, tuple):
            return result

        return jsonify({'message': 'success', 'code': 200}), 200

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
