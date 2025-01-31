from app import connect_database
from flask import jsonify, url_for
from os import path, listdir
import config, send_file
from app.background_tasks.download_gallery import download_gallery_with_object_id


def try_sending_image_with_gid_order(token: str, gid: str, order: int):
    db = connect_database.Connect.get_connection()
    print('GID: ' + gid)
    print('order: ' + str(order))
    record: dict = db.Gallery.find_one({'ex.gid': gid})
    if record is None:
        return jsonify({'msg': 'Sorry. The server does not have that on record. Please wait for about 5 minutes and '
                               'retry.'})
    object_id = str(record['_id'])
    if 'uploaded' in record and record['uploaded'] is True:
        print('File found')
        return send_image_with_gid_order(object_id, order)
    else:
        origin_url = url_for('s', token=token, gid_with_order=gid + '-' + str(order))
        task = download_gallery_with_object_id.apply_async(args=[object_id, origin_url])
        return jsonify({'msg': 'The record is found. But the file is not downloaded yet. Please wait for 1 minute '
                               'and retry.',
                        'task_url': url_for('get_status_for', task_name='download_gallery', task_id=task.id)})


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
