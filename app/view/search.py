from app.connect_database import Connect
from flask import jsonify
from bson.json_util import dumps
import requests
import json


def search(words, limit, page, filtered_category, minimum_rating, tag_list):
    db = Connect.get_connection()
    query_dict = dict()

    if tag_list:
        query_dict['tag_dict'] = {"$all": tag_list}  # Tags must contain ":"
    if words:
        query_dict['$text'] = {'$search': words}
    if filtered_category:
        query_dict['category'] = {'$ne': filtered_category}
    # start_point = page * limit
    # end_point = start_point + limit
    # query_dict['$range'] = [start_point, end_point]
    result = db.Gallery.find(query_dict).sort([("ex.upload_time", -1)]).skip(page * limit).limit(limit)
    return dumps(result)


if __name__ == '__main__':
    # input_json = request.get_json(force=True, silent=True) or {}
    # words = input_json.get('word', '')
    # #: (optional) 搜索的关键字，如果为空则返回所有结果
    # tag_list = input_json.get('tags', [])
    # #: (optional) 搜索的Tags，格式为List<Str>
    # limit = input_json.get('limit', 25)
    # #: (optional) 搜索的结果数，默认25
    # page = input_json.get('page', 0)
    # #: (optional) 第几页的内容，默认0
    # filtered_category = input_json.get('filtered', [])
    # #: (optional) 不包含的分类，格式为List<Str>
    # minimum_rating = input_json.get('minimum', 0.0)
    # #: (optional) 最低评分
    dict_json = dict(tags=['female:lolicon'])
    r = requests.post('http://127.0.0.1:5000/v1/view/searchByWords', json=dict_json)
    for record in r.json():
        print(record)
