import os
import platform
import threading
import time
import json
import shutil
import serial
from utilset.ConfigUtil import ConfigUtil


# Arduino資料接收器
# 持續從Arduino的Serial序列埠接收溫度計溫度數值資料，並寫到溫控顯示介面讀取路徑中
class ArduinoReader():

    __deviceRootPath = None
    __buzzer = None

    # 初始化，建立執行緒，每秒持續接收來自arduino serial的溫度計資料
    def __init__(self, buzzer):
        self.__deviceRootPath = ConfigUtil().DeviceRootPath
        self.__buzzer = buzzer  # 接收蜂鳴器物件，接收到Arduino連接的按鈕設備按下時，要觸發停止警報動作
        self.__initPath()  # 先執行一次讀資料動作，準備device serial資料夾
        task = threading.Thread(target=self.__task)
        task.setDaemon(True)
        task.start()

    # 執行緒本體
    def __task(self):
        while True:
            self.__readData()
            time.sleep(5)

    # 初始化溫度文件資料，每次啟動程式將__deviceRootPath資料夾移除
    def __initPath(self):
        # 根據讀取json筆數產生對應序號的檔案與資料夾路徑(仿溫度計接在樹梅派對於w1 device產生溫度的動作)
        if os.path.exists(self.__deviceRootPath) is True:
            shutil.rmtree(self.__deviceRootPath, ignore_errors=True)  # 移除舊有的device資料夾
        # 執行一次讀資料動作
        self.__readData()

    # 接收來自arduino serial的溫度計資料
    def __readData(self):
        # 從serial接收json data
        data = self.__readArduinoSerial()
        # 將json data轉成array<object>
        dataArray = json.loads(data)
        # 根據讀取json筆數產生對應序號的檔案與資料夾路徑(仿溫度計接在樹梅派對於w1 device產生溫度的動作)
        for item in dataArray:
            # 讀取相關屬性值
            temp = int(float(item["temp"]) * 1000)
            tempSerial = item["tempSerial"]
            # 開始寫入檔案
            deviceFolder = os.path.join(self.__deviceRootPath, tempSerial)
            deviceFile = os.path.join(deviceFolder, "w1_slave")
            # 檢查資料夾是否存在
            if os.path.exists(deviceFolder) is False:
                os.makedirs(deviceFolder)
            # 仿造樹梅派讀取w1設備在/sys/bus/w1/device/28-*/w1_slave檔案的寫法
            with open(deviceFile, 'w') as f:
                f.write("00 00 00 00 00 00 00 00 00 : crc=00 YES\n")
                f.write("00 00 00 00 00 00 00 00 00 t=" + str(temp))

    # 讀取來自Arduino Serial的資料
    def __readArduinoSerial(self):
        # 判斷執行環境為window，直接回傳測試資料
        if platform.system() is "Windows":
            return '[{"deviceID":1, "tempID": 0, "tempSerial":"23579A1257983476", "temp":27.53},{"deviceID":0, "tempID": 1, "tempSerial":"23579A1846783479", "temp":30.53},{"deviceID":0, "tempID": 2, "tempSerial":"53579A18A678B470", "temp":30.53}]'
