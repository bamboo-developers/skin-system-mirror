from flask import Blueprint
import skin_system

bp = Blueprint('signature_ver_keyDER', __name__)
bp2 = Blueprint('signature_ver_keyPEM', __name__)

@bp.route('/signature-verification-key.der')
@skin_system.token_required(0)
def func():
    url = f"http://skinsystem.ely.by/signature-verification-key.der"

    return skin_system.resolve(url)

@bp2.route('/signature-verification-key.pem')
@skin_system.token_required(0)
def func2():
    url = f"http://skinsystem.ely.by/signature-verification-key.pem"

    return skin_system.resolve(url)