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
        # 判斷設定檔是否存在
        if os.path.exists(self.__filePath) is False:
            messagebox.showinfo("error", "設定檔不存在。")
            exit()
        # 讀取設定檔
        config = configparser.ConfigParser()
        config.read(self.__filePath, encoding="UTF-8")
        # 讀取溫控設備設定
        self.DeviceID = json.loads(config["SystemConfig"]["DeviceID"])
        self.DeviceName = json.loads(config["SystemConfig"]["DeviceName"])
        self.TempCaptureTime = json.loads(config["SystemConfig"]["TempCaptureTime"])
        self.Thermometer = json.loads(config["SystemConfig"]["Thermometer"])