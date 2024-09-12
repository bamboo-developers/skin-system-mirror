from flask import Blueprint, request, send_from_directory, jsonify
import skin_system

bp = Blueprint('temp_save_skins', __name__)

UPLOAD_FOLDER = skin_system.get_path('temp/', "..")


@bp.route('/temp', methods=['POST'])
def upload_skin():
    file = request.files.get('file')
    time = min(int(request.form.get('time', 120)), 120)
    if not file:
        return jsonify({'message': 'No file provided', 'code': 400}), 400
    result = skin_system.temp_skin_storge(file, web=True, time=time)
    if isinstance(result, tuple):
        return result

    return result


@bp.route('/temp/get/<filename>', methods=['GET'])
def download_skin(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
