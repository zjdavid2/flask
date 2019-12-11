from flask import Blueprint, jsonify
from app.ex_extension.send_image_with_gid_order import try_sending_image_with_gid_order

extension = Blueprint('extension', __name__, url_prefix='')


@extension.route('/s/<token>/<gid_with_order>')
def s(token, gid_with_order: str):
    gid_with_order_split = gid_with_order.split('-')
    if len(gid_with_order_split) != 2:
        return jsonify({'msg': 'The gid you provided is not valid.'})
    gid: str = gid_with_order_split[0]
    try:
        order = int(gid_with_order_split[1])
    except (ValueError, TypeError):
        return jsonify({'msg': 'Your order number is invalid.'})

    return try_sending_image_with_gid_order(token, gid, order)