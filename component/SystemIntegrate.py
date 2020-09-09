# coding=UTF-8
import math
import hashlib
import json
import urllib
from utilset.ConfigUtil import ConfigUtil


# 與後台平台或其他系統整合
class SystemIntegrate():

    __URL = None

    # 初始化
    def __init__(self):
        self.__URL = ConfigUtil().PostURL

    # 發布溫度到雲端後台
    def postTemp(self, data):
        postData = self.__getPostData(data)
        # 準備要post的json
        postJson = json.dumps(postData, ensure_ascii=False)
        # 執行Post
        headers = {
            'Content-Type': 'application/json'
        }
        req = urllib.request.Request(url=self.__URL, data=postJson.encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req) as res:
            print(res.read())

    # 轉換data為介接協議之字串格式
    def __getPostData(self, data):
        postData = []
        # 讀取參數值
        for item in data:
            deviceID = item["deviceID"]
            tempID = item["tempID"]
            temp = item["temp"]
            # 組出介接協議接收處理的字串格式
            postStr = "T" + deviceID + tempID + ("+" if temp >= 0 else "") + str(round(temp, 1))
            postStr = postStr + "#" + self.__getMD5(postStr)
            postData.append({
                "code": postStr
            })
        return postData

    # 取得MD5雜湊
    def __getMD5(self, data):
        # 計算md5雜湊值
        data = data.encode("utf-8")  # 字串轉為UTF8的Bytes陣列
        MD5 = hashlib.md5()
        MD5.update(data)
        code = MD5.hexdigest()
        return code[0:4]
