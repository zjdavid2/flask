from app.connect_database import Connect
from flask import jsonify


def format_result(tag_list):
    result_dict = dict()
    for record in tag_list:
        category = record['category']
        if result_dict.get(category) is None:
            result_dict[category] = [record['name']]
        else:
            result_dict[category].append(record['name'])
    return result_dict


def get_tag_list():
    tag_list = Connect.get_connection().tags.find().sort([('occurrences', -1)]).limit(50)
    return jsonify(format_result(tag_list))


def get_tag_list_filtered_by(key_word):
    tag_list = Connect.get_connection().tags.find({'$text': {'$search': key_word}}).sort([('occurrences', -1)]).limit(50)
    return jsonify(format_result(tag_list))
