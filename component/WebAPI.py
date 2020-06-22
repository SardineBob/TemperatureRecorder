from flask import Flask, request
from component.Temperature import Temperature
from utilset.TemperatureUtil import TemperatureUtil
from datetime import datetime
import threading


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
        msg = ''
        for item in self.__temperature:
            msg += "目前時間：" + datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "，設備名稱：" + item.getName() + "，溫度攝氏：" + str(item.getTemperature()) + "度<br/>"
        return msg

    # 取得歷史溫度資料
    def getHistoryTemp(self, reqJson):
        # 先擷取request過來的參數
        date = reqJson['date']
        # 根據這個日期取得整個日期的溫度數據資料
        data = TemperatureUtil().selectTemperature(date)
        # 將array(tuple)的資料轉成json
        result = []
        for item in data:
            result.append({
                'time': item[0],
                'temp': item[1]
            })
        # response data
        return str(result)
