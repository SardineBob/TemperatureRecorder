import os
from tkinter import messagebox
import configparser
import json


# 設定檔存取元件
class ConfigUtil():

    __filePath = 'config.ini'
    TempCaptureTime = None

    def __init__(self):
        # 判斷設定檔是否存在
        if os.path.exists(self.__filePath) is False:
            messagebox.showinfo("error", "設定檔不存在。")
            exit()
        # 讀取設定檔
        config = configparser.ConfigParser()
        config.read(self.__filePath, encoding="UTF-8")
        # 讀取擷取溫度循環時間
        self.TempCaptureTime = json.loads(config["SystemConfig"]["TempCaptureTime"])