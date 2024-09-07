from flask import Blueprint, jsonify

bp = Blueprint('errors', __name__)

@bp.errorhandler(Exception)
def handle_error(e):
    status_code = 500

    if hasattr(e, 'code'):
        status_code = e.code

    return jsonify({'message': str(e)}), status_code