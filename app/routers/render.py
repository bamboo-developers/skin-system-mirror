from flask import Blueprint, Response, request, abort
from six import BytesIO
import skin_system

bp = Blueprint('render', __name__)

@bp.route('/render/<username>')
@skin_system.token_required(0)
def func(username):
    try:
        username = skin_system.DB.what_redirect_of(username, 'ely')
        url = f"http://skinsystem.ely.by/skins/{username['ely']}.png"

        skin_image = skin_system.resolv_skin(url)

        scale = min(request.args.get('scale', default=8, type=int), 100)
        type = request.args.get('type', default='body', type=str)
        layer = request.args.get('layer', default=1, type=int)

        processed_skin = skin_system.process(skin_image, scale, type, layer)

        img_io = BytesIO()
        processed_skin.save(img_io, 'PNG')
        img_io.seek(0)

        return Response(img_io, content_type='image/png')

    except Exception as e:
        print(f"An error occurred: {e}")
        abort(500, description="Internal Server Error")
