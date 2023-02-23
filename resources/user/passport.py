import json

from flask import make_response, session
from common.models.user import User
from . import user_bp
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from common.models import db


@user_bp.route("/login/account", methods=["GET", "POST"])
def index():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(name=username).first()
    resp = make_response()
    if not user:
        msg = {"status": "错误的用户名和密码"}
        resp.data = json.dumps(msg).encode('utf8')
        return resp
    res = check_password_hash(user.password, password)
    if not res:
        msg = {"status": "错误的用户名和密码"}
        resp.data = json.dumps(msg).encode('utf8')
        return resp
    msg = {"status": "ok"}
    resp.data = json.dumps(msg).encode('utf8')
    session["name"] = username
    return resp


@user_bp.route("/currentUser")
def user_info():
    username = session.get("name")
    resp = make_response()
    if not username:
        msg = {"success": False}
        resp.data = json.dumps(msg).encode('utf8')
        return resp
    user = User.query.filter_by(name=username).first()
    msg = {
        "success": True,
        "data": {
            "name": username,
            "avatar": user.avatarUrl or 'https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png'
        }}
    resp.data = json.dumps(msg).encode('utf8')
    return resp


@user_bp.route("/register/account", methods=["POST"])
def register_user():
    username = request.json.get('username')
    password = request.json.get('password')
    password_hash = generate_password_hash(password)
    user = User.query.filter_by(name=username).first()
    resp = make_response()
    if user:
        resp.status = '200 ok'
        resp.data = b'{"status": "username repeated"}'
        return resp
    user = User(name=username, password=password_hash)
    db.session.add(user)
    db.session.commit()

    resp.status = '200 ok'
    resp.headers['content-type'] = 'application/json'
    resp.data = b'{"status": "ok"}'
    session["name"] = username
    return resp
