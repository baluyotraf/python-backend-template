from flask import Blueprint, jsonify, url_for
from app.tasks.sample import sample_task

blueprint = Blueprint('sample', __name__, url_prefix='/sample')

@blueprint.route('/')
def welcome_sample_task():
    return 'welcome'

@blueprint.route('/', methods=['POST'])
def create_sample_task():
    task = sample_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('.get_sample_task', task_id=task.id)}

@blueprint.route('/<task_id>', methods=['GET'])
def get_sample_task(task_id):
    task = sample_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'current': 0
        }
    elif task.state == 'FAILURE':
        response = {
            'current': None
        }
    else:
        response = {
            'current': task.info.get('current', 0)
        }
    return jsonify(response)
