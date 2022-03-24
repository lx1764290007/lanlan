import base64
import json
from Crypto.Cipher import AES


# base64解码函数
def D_BASE64(origStr):
    # 当输入的base64字符串不是3的倍数时添加相应的=号
    if (len(origStr) % 3 == 1):
        origStr += "=="
    elif (len(origStr) % 3 == 2):
        origStr += "="
        # origStr = bytes(origStr, encoding='utf8')  # 看情况进行utf-8编码
    dStr = base64.b64decode(origStr)
    return dStr

secret = '70c76642eaea7cbaad709c1713d2784c'


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = D_BASE64(self.sessionKey)
        encryptedData = D_BASE64(encryptedData)
        iv = D_BASE64(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
