import pymysql
from model import Config as config
from vc_flask.MyFlask import app, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from vc_flask.MyFlask import app

pymysql.install_as_MySQLdb()


class Config(object):
    """配置参数"""
    # 设置连接数据库的URL
    user = config.DataBase.user
    password = config.DataBase.password
    database = config.DataBase.database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@localhost:3306/%s' % (user, password, database)
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

