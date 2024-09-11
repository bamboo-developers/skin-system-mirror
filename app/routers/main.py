import time
import datetime
from flask import Blueprint, jsonify, request

bp = Blueprint('main', __name__)

start_time = time.time()


def get_uptime():
    current_time = time.time()
    uptime_seconds = current_time - start_time
    uptime = str(datetime.timedelta(seconds=int(uptime_seconds)))
    return uptime


@bp.route('/')
def index():
    x_forwarded_for = request.headers.get('X-Forwarded-For', '')
    real_ip = x_forwarded_for.split(',')[0].strip()

    return jsonify({
        'message': 'skin-system online and ready to work',
        'code': 200,
        'uptime': get_uptime(),
        "requester's IP": real_ip
    })