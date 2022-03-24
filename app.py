from flask import Flask, jsonify, Response, request, abort
from flask_sqlalchemy import SQLAlchemy
import pymysql
from databse import Config as config
import json
from miniprogram import WXBizDataCrypt, GetSession
from urllib import parse
import hashlib
from tools import Time
import datetime
import time

app = Flask(__name__)

pymysql.install_as_MySQLdb()


class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = config.DataBase.user
    password = config.DataBase.password
    database = config.DataBase.database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@127.0.0.1:3306/%s' % (user, password, database)
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True
    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False


# 读取配置
app.config.from_object(Config)
# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


class MyResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (list, dict)):
            response = jsonify(response)
        return super(Response, cls).force_type(response, environ)


app.response_class = MyResponse


# 用户 - 模型
class SignIn(db.Model):
    # 定义表名
    tablename = 'sign_in'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_sign_in = db.Column(db.Integer, unique=True)
    boy = db.Column(db.Integer)
    girl = db.Column(db.Integer)
    __doc__: '签到信息'

    def __repr__(self):
        return 'Course:%s' % self.name


class User(db.Model):
    # 定义表名
    tablename = 'user'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    sex = db.Column(db.Integer)
    token = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    __doc__: '签到信息'

    def __repr__(self):
        return 'Course:%s' % self.name


# 纪念信息 - 模型
class Info(db.Model):
    # 定义表名
    tablename = 'info'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    perception_date = db.Column(db.Integer, unique=True)
    love_date = db.Column(db.Integer, unique=True)
    __doc__: '包含了一些相识相知的日期等'


# 初始化数据库连接
db.init_app(app)


# 对查询的结果进行格式转化
def to_json(obj):
    _dict = vars(obj)
    for i in list(_dict.keys()):
        if i.startswith('_'):
            _dict.pop(i)
    return _dict


@app.route('/info/<token>', methods=['GET'])
def get_info(token):
    # add_info = Info(perception_date=123456789, love_date=123456788)
    # db.session.add(add_info)
    # db.session.commit()
    data = json.dumps(Info.query.get(1), default=to_json)
    return Response(data, mimetype='application/json')


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
@app.route('/sign-in', methods=['POST'])
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


# 签到历史列表 - 性别
@app.route('/sign-in-history-by-sex/<token>/<sex>', methods=['GET'])
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


# 签到历史列表
@app.route('/sign-in-history/<token>', methods=['GET'])
def get_history(token):
    user = User.query.filter_by(token=token).first()
    data = []
    if user is None:
        abort(Response('抱歉，您并非受邀用户'))
    else:
        data = SignIn.query.order_by(SignIn.last_sign_in.desc()).all()

    return Response(json.dumps(data, default=to_json), mimetype='application/json')


# 签到历史查询-名字条件
@app.route('/sign-in-history-by-name/<name>', methods=['GET'])
def get_history_by_search(name):
    data = json.dumps(SignIn.query.filter_by(username=name), default=to_json)
    return Response(data, mimetype='application/json')


# 签到历史查询-日期条件
@app.route('/sign-in-today', methods=['GET'])
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
            'users': User.query.all()
        }
        return json.dumps(res, default=to_json)


@app.route('/app-login', methods=['POST'])
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


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)
