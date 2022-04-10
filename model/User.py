import json
from dao.MySql_Config import db
from model.VC_Model import User
from tools.Utils import to_json
from vc_flask.MyFlask import Response, abort


def db_handle(phone, token):
    result = User.query.filter_by(phone=phone).first()
    if result is None:
        abort(Response('抱歉，您并非受邀用户'))
    else:
        result.token = token
        db.session.commit()
        data = User.query.filter_by(phone=phone).first()
        res = {
            'data': data,
            'partner': User.query.filter_by(phone != phone).first()
        }
        return json.dumps(res, default=to_json)
