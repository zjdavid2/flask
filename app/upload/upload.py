from typing import Dict, Any, Union

from flask import Blueprint, request, jsonify
from app.upload.ipfs_hash import IPFSHash
from app.request_error import RequestError
from bson.objectid import ObjectId
from bson.errors import InvalidId
from app.upload import save_img
from app.auth.auth_tools import login_required, current_user_is_admin


upload = Blueprint('upload', __name__, url_prefix='/v1/upload')


# TODO: Authentication Required
@upload.route('/setIPFSFolderHash', methods=['POST'])
def set_IPFS_folder_hash_by_gid():
    request_json = request.get_json(force=True, silent=True) or {}
    ipfs_hash = request_json.get('ipfs_hash', '')
    #: 需要添加的 IPFS Hash 资料夹
    gid = request_json.get('gid', '')
    #: 作品的Ex Gid
    if gid:
        result = IPFSHash().update_hash_folder('ex.gid', gid, ipfs_hash)
        return result
    hash_id = request_json.get('id', '')
    #: 作品的数据库Hash id
    if hash_id:
        try:
            hash_id = ObjectId(hash_id)
            result = IPFSHash().update_hash_folder('_id', hash_id, ipfs_hash)
            return result
        except InvalidId:
            return jsonify({'msg': RequestError().invalid_hash_id()}), 400
    return jsonify({'msg': RequestError().no_unique_parameter()}), 400


# TODO: Authentication Required
@upload.route('/setIPFSImageHash', methods=['POST'])
def set_IPFS_image_hash_by_gid():
    request_json = request.get_json(force=True, silent=True) or {}
    ipfs_hash_list = request_json.get('ipfs_hash_list', None)
    #: 需要添加的 IPFS Hash 列表, list 格式
    gid = request_json.get('gid', '')
    #: 作品的Ex Gid
    if gid:
        result = IPFSHash().update_image_hash('ex.gid', gid, ipfs_hash_list)
        return result
    hash_id = request_json.get('id', '')
    #: 作品的数据库Hash id
    if hash_id:
        try:
            hash_id = ObjectId(hash_id)
            result = IPFSHash().update_image_hash('_id', hash_id, ipfs_hash_list)
            return result
        except InvalidId:
            return jsonify({'msg': RequestError().invalid_hash_id()}), 400
    return jsonify({'msg': RequestError().no_unique_parameter()}), 400


@upload.route('/directUpload/<folder_id>/<order_number>', methods=['POST'])
@login_required
def upload_directly(folder_id, order_number):
    print(request.headers)
    if not current_user_is_admin():
        return jsonify({'msg': RequestError.admin_permission_required()}), 400
    if 'file' not in request.files:
        return jsonify({'msg': RequestError.no_file_uploaded()}), 400
    file = request.files['file']
    if file.filename == '' or not file:
        return jsonify({'msg': RequestError.no_file_uploaded()}), 400
    expected_sha_1, file_extension = None, None
    if request.form:
        expected_sha_1 = request.form.get('sha1', None)  # Optionally check sha1 of the image.
        file_extension = request.form.get('extension', None)
    return save_img.save_img(file, folder_id, order_number, expected_sha_1, file_extension)


@upload.route('/uploadRecord', methods=['POST'])
@login_required
def upload_records():
    request_json: dict = request.get_json(force=True, silent=True) or {}
    if len(request_json) == 0:
        return jsonify({'msg': RequestError('json').required_parameter_not_found()})
    return 'Method not implemented!'

