import datetime
import json
import time
from dao.MySql_Config import db
from tools import Time
from tools.Utils import to_json
from vc_flask.MyFlask import app, Response, request, abort
from model.VC_Model import SignIn, User


def insert_sign(is_boy):
    sign_in_record = SignIn.query.all()[-1]
    if sign_in_record.boy == 1 or sign_in_record.girl == 1:
        abort(Response('已经签过了'))
    if is_boy > 0:
        sign_in_record.boy = 1
    else:
        sign_in_record.girl = 1


def add_sign(is_boy, date):
    if is_boy > 0:
        sign_add = SignIn(last_sign_in=date, boy=1, girl=0)
        db.session.add(sign_add)
    else:
        sign_add = SignIn(last_sign_in=date, boy=0, girl=1)
        db.session.add(sign_add)


# 签到
def sign_in():
    data = request.get_json()
    token = data.get('token')
    date = data.get('date')
    user = User.query.filter_by(token=token).first()
    is_boy = user.sex
    sign_in_record = SignIn.query.all()
    if user is None:
        abort(Response('抱歉，您并非受邀用户'))
    else:
        # 检查是否新一天签到
        if len(sign_in_record) < 1 or (
                len(sign_in_record) > 0 and
                Time.is_today(sign_in_record[-1].last_sign_in, date) is False):
            add_sign(is_boy, date)
        else:
            insert_sign(is_boy)
        db.session.commit()
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
