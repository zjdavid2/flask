from flask import Blueprint, jsonify
from app.background_tasks.download_gallery import download_gallery_with_object_id

background_tasks = Blueprint('background_tasks', __name__, url_prefix='v1/background')


@background_tasks.route('/get_status_for/<task_name>/<task_id>')
def get_status_for(task_name: str, task_id: str):
    if task_name == 'download_gallery':
        task = download_gallery_with_object_id
    else:
        return jsonify({'msg': 'The task name is invalid.'})
    task_result = task.AsyncResult(task_id)
    if task_result.state == 'PENDING':
        # job did not start yet
        return jsonify({'status': 'PENDING'})
    elif task.state != 'FAILURE':
        response = {
            'state': task_result.state,
            'status': task_result.info.get('status', '')
        }

        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)