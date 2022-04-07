import hashlib
import json
from urllib import parse
from miniprogram import WXBizDataCrypt, GetSession
from vc_flask.MyFlask import Response, request
from model.User import db_handle


def get_code():
    data = request.get_json()
    code = data.get('code')
    secret = WXBizDataCrypt.secret
    encrypted_data = parse.unquote(data.get("encryptedData"))
    iv = data.get("iv")
    app_id = data.get('appId')
    # 微信 session_key url
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {'appid': app_id, 'secret': secret, 'js_code': code, 'grant_type': 'authorization_code'}
    # 从微信服务器交换 session_key
    result = GetSession.get_session(url, params)
    # 文本 -> dict
    dict_result = json.loads(result.text)
    # 微信解密算法
    pc = WXBizDataCrypt.WXBizDataCrypt(app_id, dict_result['session_key'].strip())
    res = pc.decrypt(encrypted_data, iv)
    phone = str(res.get('phoneNumber'))
    token = hashlib.sha1(phone.encode('utf-8', 'replace')).hexdigest()
    # 数据库层
    return Response(db_handle(phone=phone, token=token), mimetype='application/json')