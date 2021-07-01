from flask import Blueprint, request, jsonify
from .s3.service import S3Service


upload_blueprint = Blueprint('upload', __name__)


@upload_blueprint.route('/upload', methods=['POST', 'PUT'])
def upload():
    file = request.files.get('file')
    acl = request.args.get('acl', None) or \
        request.form.get('acl', 'public-read')
    bucket_name = request.args.get('bucket_name', None) or \
        request.form.get('bucket_name', None)
    path = request.args.get('path', None) or request.form.get('path', None)

    if acl == 'public':
        acl = 'public-read'

    if file is None:
        return jsonify(
            '''No file founded, send your file using a form-data in a field
            named \'file\''''
        ), 400

    rsp = S3Service.upload(file, bucket_name=bucket_name, acl=acl, path=path)

    return jsonify({
        'url': rsp['url'],
        'key': rsp['key'],
        'bucket_name': rsp['bucket_name'],
        'path': rsp['path'],
        'acl': rsp['acl']
    })
