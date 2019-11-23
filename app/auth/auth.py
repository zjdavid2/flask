from flask import Blueprint, request, jsonify, g
import jwt
import datetime
from app.auth.auth_tools import is_username_exist, verify_sing, get_user_with_username, sign
import bcrypt
from config import Config

auth_blueprint = Blueprint(
    "auth_v1",
    __name__,
    url_prefix='/v1/auth'
)


@auth_blueprint.route('/sign_up', methods=['POST'])
def sign_up():
    if not Config.REGISTER_ENABLED:
        return jsonify({"msg": "Register is not enabled."}), 400
    try:
        username = request.form["username"]  # 要求3字以上好了
        password = request.form["password"]  # 要求8字以上好了
        email = request.form["email"]
    except KeyError:
        return jsonify({"msg": "Miss parameter"}), 400
    if len(username) < 3 or len(password) < 8:
        return jsonify({"msg": "Username or password is too short"}), 400
    if is_username_exist(username):
        return jsonify({"msg": "User Exist"}), 400  # 我應該建立一個狀態碼
    apply_data = {
        "username": username,
        "password": password,
        "email": email,
        "it": int(datetime.datetime.now().timestamp()),
        "for": "sign_config_accept",
    }
    print(apply_data)
    signed = sign(apply_data)
    return jsonify({
        "msg": "successful",
        "jwt": signed
    }), 200


@auth_blueprint.route('/sign_up_accept')
def sign_config_accept():
    try:
        code: str = request.args["auth_code"]
        auth_code: dict = verify_sing(code)
    except KeyError:
        return jsonify({"msg": "Miss token"}), 400
    except jwt.exceptions.InvalidTokenError:
        return jsonify({"msg": "Token broken"}), 400
    if auth_code.get('for') != "sign_config_accept":
        return jsonify({"msg": "Miss token"}), 400
    if int(datetime.datetime.now().timestamp()) - 60 * 60 * 24 * 2 > auth_code['it']:  # 60*60*24*2是兩天的意思
        return jsonify({"msg": "Token expired"}), 403
    try:
        username = auth_code["username"]
        password_hash = auth_code["password"]
        mail = auth_code['email']
    except KeyError:
        return jsonify({"msg": "Token does not contain required data"}), 400
    if is_username_exist(username):
        return jsonify({"msg": "User exist"}), 409
    insert_user = {
        'username': username,
        'password': password_hash,
        'application_password': [],
        'email': mail,
        "group": [],
        'email_verified': True,
        'email_change_lock': datetime.datetime.now(),
        'create_time': datetime.datetime.now(),
        'valid_since': datetime.datetime.now(),
        'enabled': True
    }
    result = g.db.users.insert_one(insert_user)
    if not result.acknowledged:
        return jsonify({"msg": "Account create failed"}), 500
    else:
        return jsonify({
            "msg": "Create successful",
            "id": str(result.inserted_id),
        }), 200


@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        username = request.form["username"]
        password: str = request.form["password"]
    except KeyError:
        return jsonify({"mag": "Username or Password is incorrect"}), 403
    if is_username_exist(username) is False:
        return jsonify({"mag": "Username or Password is incorrect"}), 403
    user = get_user_with_username(username)
    if user is None:
        return jsonify({"mag": "Username or Password is incorrect"}), 403
    hash_pwd: str = user["password"]
    if not bcrypt.checkpw(password.encode(), hash_pwd.encode()):
        return jsonify({"mag": "Username or Password is incorrect"}), 403
    user_id: str = str(user["_id"])
    token = {
        "sub": user_id,
        "iss": Config.DOMAIN_NAME,
        "aud": Config.FRONTEND_DOMAIN_NAME,
        "iat": int(datetime.datetime.now().timestamp()),
        "remember": True,
        "type": "login_credential",
        "level": "master_password"
    }
    signed = sign(token)
    return jsonify({
        "msg": "successful",
        "jwt": signed
    }), 200


@auth_blueprint.route('/forget_pwd')
def forget_pwd():
    pass
