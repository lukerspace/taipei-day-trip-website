import sys
sys.path.append("..")
from flask import *
from flask import session
from sql import cursor, conn, user_select, user_insert

appUser = Blueprint('appUser', __name__)

# appUser.secret_key="hello"

@appUser.route('/user', methods=['GET'])
def get_userdata():
    # 登入成功
    if "user" in session:
        user = session['user']
        data = {
            "data":user
        }
        return jsonify(data)

    # 登入失敗
    data = {"data": None}
    return jsonify(data)


@appUser.route('/user', methods=['POST'])
def signup():
    try:
        conn.reconnect(attempts=1, delay=0)
        data = request.json
        name = data['name']
        email = data['email']
        password = data['password']
        exist_user = user_select(email=email)

        # 註冊成功
        if not exist_user:
            user_insert(name=name, email=email, password=password)
            data = {"ok": True}
            return jsonify(data), 200

        # 如果已經有人使用過該email，回應錯誤訊息
        else:
            data = {
                "error": True,
                "message": "註冊失敗，該email已經被註冊過了"
            }
            return jsonify(data), 400

    # 伺服器錯誤
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(data), 500


@appUser.route('/user', methods=['PATCH'])
def signin():
    try:
        conn.reconnect(attempts=1, delay=0)
        data = request.json
        email = data['email']
        password = data['password']
        user = user_select(email=email, password=password)

        # 登入成功
        if user:
            session['user'] = {"id": user["id"],"name": user["name"],"email": user["email"]}
            data = {"ok": True}
            return jsonify(data)

        # 登入失敗
        else:
            data = {
                "error": True,
            }
            return jsonify(data), 200

    # 伺服器錯誤
    except:
        data = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(data), 500


@appUser.route('/user', methods=['DELETE'])
def singout():
    # 登出
    data = {"ok": True}
    session.pop('user')
    return jsonify(data)