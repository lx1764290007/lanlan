from dao.MySql_Config import db, app


# 用户 - 模型
class SignIn(db.Model):
    # 定义表名
    tablename = 'sign_in'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_sign_in = db.Column(db.Integer, unique=True)
    boy = db.Column(db.Integer)
    girl = db.Column(db.Integer)

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


db.init_app(app)
