import json
from vc_flask.MyFlask import Response
from model.VC_Model import Info
from tools.Utils import to_json


# 获取纪念信息
def get_info(token):
    data = json.dumps(Info.query.get(1), default=to_json)
    return Response(data, mimetype='application/json')
