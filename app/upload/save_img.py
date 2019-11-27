import os
from config import Config
from bson.objectid import ObjectId
from app.view.view import get_detail_common
from flask import jsonify
from app.request_error import RequestError
import glob
from app.connect_database import Connect
from pymongo.results import UpdateResult
import hashlib


def save_img(img, folder: str, order: str, expected_sha_1=None):
    hash_id = ObjectId(folder)
    result: dict = get_detail_common.get_detail_raw('_id', hash_id)
    if not result:  # 如果Object ID不合法或不存在
        return jsonify({'msg': RequestError.invalid_hash_id()}), 400

    expected_file_count: int = result['file_count']
    order_int = int(order)
    if order_int is None:
        return jsonify({'msg': RequestError('Order number').parameter_invalid()}), 400
    dir_path = Config.UPLOAD_FOLDER + "/" + folder
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    filename = order + '.jpg'
    img_path = os.path.join(dir_path, filename)
    img.save(img_path)

    if expected_sha_1:
        found_sha1 = sha1(img_path)
        if found_sha1 != expected_sha_1:
            return jsonify({'msg': 'Sha1 does not match'}), 400
        # print('SHA1 check passed.')

    if len(glob.glob1(dir_path, '*.jpg')) == expected_file_count:
        result_update: UpdateResult = Connect.get_connection().Gallery.update_one(
            {'_id': hash_id},
            {"$set": {"file_count_matches": True}})
    else:
        result_update: UpdateResult = Connect.get_connection().Gallery.update_one(
            {'_id': hash_id},
            {"$set": {"file_count_matches": False}})
    print(result_update.modified_count)

    if order_int >= expected_file_count:
        return jsonify({'msg': RequestError.file_number_too_big()}), 200
    return jsonify({'msg': 'Img successfully uploaded'}), 200


def str_to_int(string):
    try:
        int_converted = int(string)
        return int_converted
    except ValueError:
        return None


def sha1(this_file_name):
    hash_sha1 = hashlib.sha1()
    with open(this_file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()
