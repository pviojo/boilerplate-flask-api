from flask import Blueprint, jsonify, request
from .service import UserService

from project.common.decorators import require_user

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/user/create', methods=['POST'])
def create() -> dict:
    user = request.json
    rsp = UserService.register(user)

    if rsp and rsp.get('status', None) == 'ok':
        return jsonify(rsp.get('user')), 200
    else:
        return {
            'msg': 'User Not stored: {}'.format(rsp['exception'] if 'exception' in rsp else '')
        }, 400

@users_blueprint.route('/user/forget_password', methods=['POST'])
def forget_password() -> dict:
    user = request.json
    UserService.forget_password(user)

    return 'ack', 201

@users_blueprint.route('/user/change_password', methods=['PUT'])
def change_password() -> dict:
    data = request.json
    if not 'token' in data:
        return {
            'msg': 'User Pass Not changed: No token'
        }, 400

    user = UserService.get_user_from_token(data.get('token'))
    if not user:
        return {
            'msg': 'User Pass Not changed: No user'
        }, 400        

    rsp = UserService.change_password(id=user.get('id'), password=data.get('password'))
    
    if rsp and rsp.get('status', None) == 'ok' and 'token' in rsp:
        return {
            'token': rsp.get('token'),
            'user': rsp.get('user'),
        }, 200
    else:
        return {
            'msg': 'User Pass Not changed: {}'.format(rsp.get('exception', ''))
        }, 400        


@users_blueprint.route('/user/login', methods=['POST'])
@users_blueprint.route('/login', methods=['POST'])
def login() -> dict:
    user = request.json
    rsp = UserService.login(user)
    print(rsp)
    if rsp and rsp.get('status', None) == 'ok' and 'token' in rsp:
        return {
            'token': rsp.get('token'),
            'user': rsp.get('user'),
        }, 200
    else:
        return '', 401


@users_blueprint.route('/user/logout', methods=['POST'])
@users_blueprint.route('/logout', methods=['POST'])
@require_user
def logout(user, token) -> dict:
    UserService.blacklist_token(token)
    return '', 200


@users_blueprint.route('/user/me', methods=['GET'])
@require_user
def me(user, token) -> dict:
    return user, 200

