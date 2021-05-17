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
    DeviceRootPath = None
    TempCaptureTime = None
    Thermometer = None
    PostURL = None

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
        self.DeviceRootPath = json.loads(config["SystemConfig"]["DeviceRootPath"])
        self.TempCaptureTime = json.loads(config["SystemConfig"]["TempCaptureTime"])
        self.Thermometer = json.loads(config["SystemConfig"]["Thermometer"])
        self.PostURL = json.loads(config["SystemConfig"]["PostURL"])

    # 提供外部呼叫設定檔存檔
    def save(self):
        self.__saveConfig({
            "deviceID": self.DeviceID,
            "deviceName": self.DeviceName,
            "deviceRootPath": self.DeviceRootPath,
            "tempCaptureTime": self.TempCaptureTime,
            "thermometer": self.Thermometer,
            "postURL": self.PostURL,
        })

    # 設定檔存檔
    def __saveConfig(self, para):
        # 讀取設定參數
        deviceID = para["deviceID"]
        deviceName = para["deviceName"]
        deviceRootPath = para["deviceRootPath"]
        tempCaptureTime = para["tempCaptureTime"]
        thermometer = para["thermometer"]
        postURL = para["postURL"]
        # 產生設定檔物件
        config = configparser.ConfigParser()
        # 產生系統設定參數
        config['SystemConfig'] = {
            'DeviceID': json.dumps(deviceID, ensure_ascii=False),
            'DeviceName': json.dumps(deviceName, ensure_ascii=False),
            'DeviceRootPath': json.dumps(deviceRootPath, ensure_ascii=False),
            'TempCaptureTime': json.dumps(tempCaptureTime),  # 擷取溫度循環時間，每N秒，讀取溫度，並寫入溫度紀錄
            'Thermometer': json.dumps(thermometer, ensure_ascii=False),  # 溫度計硬體設備序號與名稱(陣列)
            'PostURL': json.dumps(postURL, ensure_ascii=False),  # 要發布溫度到後台的網址
        }
        # 寫入設定檔
        with open(self.__filePath, 'w', encoding='UTF8') as configFile:
            config.write(configFile)

    # 初始化設定檔
    def __initConfig(self):
        return {
            "deviceID": "0000",
            "deviceName": "星堡保全",
            "deviceRootPath": "/sys/bus/w1/devices/",
            "tempCaptureTime": 60,
            "thermometer": [
                {'id': 'A01', 'name': '左邊冷凍櫃', 'serial': '28531F7D613CED', 'initTemp': 20, 'uplimit': 25, 'lowlimit': -10},
                {'id': 'A02', 'name': '中間冷凍櫃', 'serial': '28CEBD7D613CA6', 'initTemp': 10,  'uplimit': 15, 'lowlimit': 5},
                {'id': 'A03', 'name': '右邊冷凍櫃', 'serial': '28177A7D613C87', 'initTemp': 60,  'uplimit': 70, 'lowlimit': 50},
            ],
            "postURL": "http://59.125.33.102:2028"
        }
