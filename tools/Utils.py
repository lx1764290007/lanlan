# 对查询的结果进行格式转化
def to_json(obj):
    _dict = vars(obj)
    for i in list(_dict.keys()):
        if i.startswith('_'):
            _dict.pop(i)
    return _dict