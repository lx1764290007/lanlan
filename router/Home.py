from model import Info as Inf, Sign as Sig, Miniprogram_Screct
from vc_flask.MyFlask import app, request
from upload_file.upload import done


@app.route('/info/<token>', methods=['GET'])
def get_info(token):
    # add_info = Info(perception_date=123456789, love_date=123456788)
    # db.session.add(add_info)
    # db.session.commit()
    return Inf.get_info(token)


# 执行签到
@app.route('/sign-in', methods=['POST'])
def sign_in():
    return Sig.sign_in()


# 签到历史列表 - 性别
@app.route('/sign-in-history-by-sex/<token>/<sex>', methods=['GET'])
def get_sign_by_sex(token, sex):
    return Sig.get_history_sex(token, sex)


# 签到历史列表
@app.route('/sign-in-history/<token>', methods=['GET'])
def get_history(token):
    return Sig.get_history_list(token)


# 签到历史查询-名字条件
@app.route('/sign-in-history-by-name/<name>', methods=['GET'])
def get_history_by_search(name):
    return Sig.get_history_by_search(name)


# 签到历史查询-日期条件
@app.route('/sign-in-today', methods=['GET'])
def get_today_history():
    return Sig.get_today_history()


@app.route('/app-login', methods=['POST'])
def get_code():
    return Miniprogram_Screct.get_code()


@app.route('/pics-upload', methods=['POST'])
def upload():
    # file = request.files.get('pic')
    # print(file)
    return done()
