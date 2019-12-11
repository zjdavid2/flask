from app import connect_database
from flask import jsonify
from os import path, listdir
import config, send_file
from bson import ObjectId
from uploader.download_using_archiver_key import download_using_archiver_key
from uploader.scan_and_upload_img import ScanAndUpload
from threading import Thread


def try_sending_image_with_gid_order(gid: str, order: int):
    db = connect_database.Connect.get_connection()
    print('GID: ' + gid)
    print('order: ' + str(order))
    record = db.Gallery.find_one({'ex.gid': gid})
    if record is None:
        return jsonify({'msg': 'Sorry. The server does not have that on record. Please wait for about 5 minutes and '
                               'retry.'})
    object_id = str(record['_id'])
    if record['uploaded'] is True:
        print('File found')
        return send_image_with_gid_order(object_id, order)
    else:
        thread = Thread(target=download_gallery_with_object_id, args=(object_id,))
        thread.daemon = True
        thread.start()
        return jsonify({'msg': 'The record is found. But the file is not downloaded yet. Please wait for 1-3 minutes '
                               'and retry.'})


def send_image_with_gid_order(object_id: str, order: int):
    directory = config.Config.UPLOAD_FOLDER + '/' + object_id
    image_name = str(order - 1)
    extension_list = ['.jpg', '.png', ',gif']
    extension_index = 0
    full_image_name = image_name + extension_list[extension_index]
    
    while not path.exists(directory + '/' + full_image_name):
        extension_index += 1
        if extension_index >= 3:
            return jsonify({'msg': 'The file is not found.'})
        full_image_name = image_name + extension_list[extension_index]\

    return send_file.send_file_from_directory('../' + directory, full_image_name)


def download_gallery_with_object_id(object_id_str: str):
    object_id = ObjectId(object_id_str)
    record = connect_database.Connect.get_connection().Gallery.find_one({'_id': object_id})
    download_using_archiver_key(record)
    ScanAndUpload().upload_all_named_hash_id_in_directory()
