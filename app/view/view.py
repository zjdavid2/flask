from flask import Blueprint, request, jsonify
from app import get_tag_list
from app.view import search, get_detail_common
from bson.objectid import ObjectId
from app.request_error import RequestError

view = Blueprint('view', __name__, url_prefix='/v1/view')


@view.route('/searchByWords', methods=['POST'])
def search_by_words():
    """ 主要搜索API """
    input_json = request.get_json(force=True, silent=True) or {}
    words = input_json.get('word', '')
    #: (optional) 搜索的关键字，如果为空则返回所有结果
    tag_list = input_json.get('tags', [])
    #: (optional) 搜索的Tags，格式为List<Str>
    limit = input_json.get('limit', 25)
    #: (optional) 搜索的结果数，默认25
    page = input_json.get('page', 0)
    #: (optional) 第几页的内容，默认0
    filtered_category = input_json.get('filtered', [])
    #: (optional) 不包含的分类，格式为List<Str>
    minimum_rating = input_json.get('minimum', 0.0)
    #: (optional) 最低评分
    return search.search(words, limit, page, filtered_category, minimum_rating, tag_list)


@view.route('/getDetail')
def get_detail():
    gid = request.args.get('gid', '')
    if gid:
        return get_detail_common.get_detail_common('ex.gid', gid)

    hash_id = request.args.get('id', '')
    if hash_id:
        hash_id = ObjectId(hash_id)
        return get_detail_common.get_detail_common('_id', hash_id)

    title = request.args.get('title', '')
    if title:
        return get_detail_common.get_detail_common('title', title)

    japan_title = request.args.get('japanTitle', '')
    if japan_title:
        return get_detail_common.get_detail_common('japan_title', japan_title)

    return jsonify({'msg': RequestError().no_unique_parameter()})


@view.route('/getTagList')
def get_full_tag_list():
    name = request.args.get('name', '')
    if not name:
        return get_tag_list.get_tag_list()
    else:
        return get_tag_list.get_tag_list_filtered_by(name)
