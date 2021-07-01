from flask import Blueprint, jsonify, request
from .service import SubscriberService

from project.common.decorators import require_user

subscribers_blueprint = Blueprint('subscribers', __name__)


@subscribers_blueprint.route('/subscriber/create', methods=['POST'])
def create() -> dict:
    subscriber = request.json

    rsp = SubscriberService.create(subscriber)

    if rsp and 'status' in rsp and rsp.get('status') == 'ok':
        return jsonify(rsp['subscriber']), 200
    else:
        return {
            'msg': 'Subscriber Not created: {}'.format(rsp.get('exception') if 'exception' in rsp else ''),
            'error': rsp.get('exception'),
        }, 400


@subscribers_blueprint.route('/subscriber/confirm/<string:email>/<string:hash>', methods=['PUT'])
def confirm(email, hash) -> dict:
    subscriber = SubscriberService.confirm(email=email, hash=hash)
    if not subscriber:
        return jsonify(None), 400
    
    return jsonify(subscriber.json()), 200


@subscribers_blueprint.route('/subscriber/unsubscribe/<string:email>/<string:hash>', methods=['PUT'])
def unsubscribe(email, hash) -> dict:
    subscriber = SubscriberService.unsubscribe(email=email, hash=hash)
    if not subscriber:
        return jsonify(None), 400
    
    return jsonify(subscriber.json()), 200


@subscribers_blueprint.route('/subscribers', methods=['GET'])
@require_user
def subscribers(user, token) -> dict:
    subscribers = SubscriberService.get(filter_status=['CONFIRMED'])
    return jsonify([s.json() for s in subscribers]), 200

