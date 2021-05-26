from flask import Blueprint

heartbeat_blueprint = Blueprint('heartbeat', __name__)


@heartbeat_blueprint.route('/heartbeat', methods=['GET'])
def check() -> dict:
    return {
        'status': 'ok'
    }, 200
