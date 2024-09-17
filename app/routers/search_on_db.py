from flask import Blueprint, jsonify, request
import skin_system

bp = Blueprint('search_on_db', __name__)

@bp.route('/db/search/<args>')
@skin_system.token_required(1)
def func(args):
    db_type = request.args.get('table')
    if not db_type:
        return jsonify({'message': 'parameter "table" is required', 'code': 400}), 400
    if db_type != 'user_data' and db_type != 'skin_data':
        return jsonify({'message': f'invalid table: {db_type}', 'code': 422}), 422

    if args != "<all>":
        for nick in [args]:
            if not skin_system.valid_minecraft_nick(nick):
                return jsonify({'message': f'invalid nickname: {nick}', 'code': 422}), 422

    if db_type == 'skin_data':
        return skin_system.DB.view_on_db('skin_data', skin_id=args)

    return skin_system.DB.view_on_db('user_data', nickname=args, user_id=args)
