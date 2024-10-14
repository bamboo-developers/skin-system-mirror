from flask import Blueprint, Response, jsonify, request
from six import BytesIO
import skin_system

y_allowed = ["front", "back"]
z_allowed = ["up", "down"]

bp = Blueprint('perspective_render', __name__)

@bp.route('/perspective/<username>')
@skin_system.token_required(0)
def func(username):
    username = skin_system.DB.what_redirect_of(username, 'ely')

    url = f"http://skinsystem.ely.by/skins/{username['ely']}.png"

    skin_image = skin_system.resolv_skin(url)

    if skin_image is None:
         return jsonify({'message': 'skin not found', 'code': 404}), 404

    scale = min(request.args.get('scale', default=8, type=int), 100)
    y = request.args.get('y', default='front', type=str)
    z = request.args.get('z', default='up', type=str)

    if y not in y_allowed or z not in z_allowed:
            return jsonify({"message": "Invalid parameters", "code": 400}), 400

    processed_skin = skin_system.perspective(skin_image, scale, y, z)

    img_io = BytesIO()
    processed_skin.save(img_io, 'PNG')
    img_io.seek(0)

    return Response(img_io, content_type='image/png')