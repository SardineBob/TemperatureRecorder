# coding=UTF-8
import os
from tkinter import messagebox
import configparser
import json


# 設定檔存取元件
class ConfigUtil():

    __filePath = 'config.ini'
    DeviceID = None
    DeviceName = None
    TempCaptureTime = None
    Thermometer = None

    def __init__(self):
        # 判斷設定檔是否存在，不存在則給予預設參數值
        if os.path.exists(self.__filePath) is False:
            self.__saveConfig(self.__initConfig())
        # 讀取設定檔
        config = configparser.ConfigParser()
        config.read(self.__filePath, encoding="UTF-8")
        # 讀取溫控設備設定
        self.DeviceID = json.loads(config["SystemConfig"]["DeviceID"])
        self.DeviceName = json.loads(config["SystemConfig"]["DeviceName"])
        self.TempCaptureTime = json.loads(config["SystemConfig"]["TempCaptureTime"])
        self.Thermometer = json.loads(config["SystemConfig"]["Thermometer"])

    # 提供外部呼叫設定檔存檔
    def save(self):
        self.__saveConfig({
            "deviceID": self.DeviceID,
            "deviceName": self.DeviceName,
            "tempCaptureTime": self.TempCaptureTime,
            "thermometer": self.Thermometer,
        })

    # 設定檔存檔
    def __saveConfig(self, para):
        # 讀取設定參數
        deviceID = para["deviceID"]
        deviceName = para["deviceName"]
        tempCaptureTime = para["tempCaptureTime"]
        thermometer = para["thermometer"]
        # 產生設定檔物件
        config = configparser.ConfigParser()
        # 產生系統設定參數
        config['SystemConfig'] = {
            'DeviceID': json.dumps(deviceID, ensure_ascii=False),
            'DeviceName': json.dumps(deviceName, ensure_ascii=False),
            'TempCaptureTime': json.dumps(tempCaptureTime),  # 擷取溫度循環時間，每N秒，讀取溫度，並寫入溫度紀錄
            'Thermometer': json.dumps(thermometer, ensure_ascii=False),  # 溫度計硬體設備序號與名稱(陣列)
        }
        # 寫入設定檔
        with open(self.__filePath, 'w', encoding='UTF8') as configFile:
            config.write(configFile)

    # 初始化設定檔
    def __initConfig(self):
        return {
            "deviceID": "0001",
            "deviceName": "南臺灣分店",
            "tempCaptureTime": 6,
            "thermometer": [
                {'id': 'A01', 'name': '左邊冷凍櫃', 'serial': '28-041694bd1cff', 'uplimit': 15, 'lowlimit': -5},
                {'id': 'A02', 'name': '中間冷凍櫃', 'serial': '28-041694bd1cfg', 'uplimit': 30, 'lowlimit': 27},
                {'id': 'A03', 'name': '右邊冷凍櫃', 'serial': '28-041694bd1cfh', 'uplimit': 10, 'lowlimit': 9},
            ]
        }
