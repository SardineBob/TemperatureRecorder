from flask import Flask, request
from component.Temperature import Temperature
from utilset.TemperatureUtil import TemperatureUtil
from datetime import datetime
import threading
import json


class WebAPI():

    __port = 9453
    __temperature = None

    def __init__(self, para):
        # 取得需使用的參數或物件
        self.__temperature = para['temperature']
        # 建立執行序跑WebAPI服務
        task = threading.Thread(target=self.__start)
        task.setDaemon(True)
        task.start()

    # 建立WebAPI服務
    def __start(self):
        app = Flask(__name__)
        # mapping router
        # 取得目前溫度
        @app.route("/getNowTemperature", methods=['GET'])
        def getNowTemperature():
            return self.getNowTemperature()
        # 取得歷史溫度資料
        @app.route("/getHistoryTemp", methods=['GET'])
        def getHistoryTemp():
            return self.getHistoryTemp(request.json)

        app.run(port=self.__port)

    # 取得目前溫度
    def getNowTemperature(self):
        result = []
        for item in self.__temperature:
            result.append({
                'now': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                'name': item.getName(),
                'temperature': item.getTemperature()
            })
        return json.dumps(result, ensure_ascii=False)

    # 取得歷史溫度資料
    def getHistoryTemp(self, reqJson):
        # 根據查詢條件取得符合的溫度數據資料
        data = TemperatureUtil().selectTemperature(reqJson)
        return json.dumps(data, ensure_ascii=False)
