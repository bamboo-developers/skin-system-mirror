from flask import Blueprint, Response, jsonify, request
from six import BytesIO
from werkzeug.exceptions import HTTPException
import skin_system

bp = Blueprint('render', __name__)

@bp.route('/render/<username>')
@skin_system.token_required(0)
@bp.errorhandler(HTTPException)
def func(username):
    username = skin_system.what_redirect_of(username)

    url = f"http://skinsystem.ely.by/skins/{username}.png"

    skin_image = skin_system.resolv_skin(url)

    if skin_image is None:
         return jsonify({'message': f'skin not found', 'code': 404}), 404

    scale = min(request.args.get('scale', default=8, type=int,), 100)
    type = request.args.get('type', default='body', type=str)
    layer = request.args.get('layer', default=1, type=int)

    processed_skin = skin_system.process(skin_image, scale, type, layer)

    img_io = BytesIO()
    processed_skin.save(img_io, 'PNG')
    img_io.seek(0)

    return Response(img_io, content_type='image/png')