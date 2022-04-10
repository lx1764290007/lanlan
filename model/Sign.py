import datetime
import json
import time
from dao.MySql_Config import db
from tools.Utils import to_json
from vc_flask.MyFlask import app, Response, request, abort
from model.VC_Model import SignIn, User


def insert_sign(token):
    sign_in_record = SignIn.query.all()[-1]
    _token_str = sign_in_record.sign_user
    if _token_str is not None:
        _token_list = _token_str.split(',')
        if token in _token_list:
            abort('已经签到过啦')
        else:
            _token_list.append(token)
            sign_in_record.sign_user = ','.join(_token_list)
            db.session.commit()
    else:
        sign_in_record.sign_user = token
        db.session.commit()
    db.session.close()


def auto_add_record():
    print('444')
    t = time.time()
    record = SignIn(last_sign_in=t, sign_user=None)
    db.session.add(record)
    db.session.commit()
    db.session.close()


# 签到
def sign_in(token):
    user = User.query.filter_by(token=token).first()
    if user is None:
        abort(Response('抱歉，您并非受邀用户'))
    else:
        insert_sign(token)
    return Response('ok', mimetype='application/json')


def get_history_sex(token, sex):
    user = User.query.filter_by(token=token).first()
    data = []
    if user is None:
        abort(Response('抱歉，您并非受邀用户'))
    if sex is None:
        data = json.dumps(SignIn.query.all(), default=to_json)
    else:
        if sex == 'boy':
            data = json.dumps(SignIn.query.filter_by(boy=1).all(), default=to_json)
        else:
            data = json.dumps(SignIn.query.filter_by(girl=1).all(), default=to_json)
    return Response(data, mimetype='application/json')


def get_history_list(token):
    user = User.query.filter_by(token=token).first()
    data = []
    if user is None:
        abort(Response('抱歉，您并非受邀用户'))
    else:
        data = SignIn.query.order_by(SignIn.last_sign_in.desc()).all()

    return Response(json.dumps(data, default=to_json), mimetype='application/json')


def get_history_by_search(name):
    data = json.dumps(SignIn.query.filter_by(username=name), default=to_json)
    return Response(data, mimetype='application/json')


def get_today_history():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    # 昨天结束时间戳
    yesterday_end_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) - 1
    today_start_time = yesterday_end_time + 1
    today_end_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) - 1
    print(today_start_time, today_end_time)
    data = json.dumps(SignIn.query.filter(SignIn.last_sign_in < today_end_time,
                                          today_start_time < SignIn.last_sign_in).first(), default=to_json)
    return Response(data, mimetype='application/json')
