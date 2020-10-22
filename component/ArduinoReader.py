import os
import platform
import threading
import time
import json
import shutil
import serial
from utilset.ConfigUtil import ConfigUtil
from tkinter import messagebox


# Arduino資料接收器
# 持續從Arduino的Serial序列埠接收溫度計溫度數值資料，並寫到溫控顯示介面讀取路徑中
class ArduinoReader():

    __deviceRootPath = None
    __buzzer = None
    __serial = None
    __serialData = None  # 來自arsuino serial溫度資料，每次讀一行，並始終覆蓋至最新
    __initSuccess = False

    # 初始化，建立執行緒，每秒持續接收來自arduino serial的溫度計資料
    def __init__(self, buzzer):
        self.__deviceRootPath = ConfigUtil().DeviceRootPath
        self.__buzzer = buzzer  # 接收蜂鳴器物件，接收到Arduino連接的按鈕設備按下時，要觸發停止警報動作
        self.__initSerial()  # 初始化序列埠
        self.__initTempFile()  # 初始化溫度文件
        # 對arduino serial監聽執行緒，每0.1秒接收一次資料
        serialListenTask = threading.Thread(target=self.__arduinoSerialListen)
        serialListenTask.setDaemon(True)
        serialListenTask.start()
        # 啟動每秒更新將溫度值，仿樹梅派w1 device作法寫入溫度文件
        updateTempTask = threading.Thread(target=self.__updateTempFile)
        updateTempTask.setDaemon(True)
        updateTempTask.start()
        # 等待，直到溫度文件初始化完成，才算物件實體化完成
        while self.__initSuccess is False:
            time.sleep(0.5)

    # 初始化序列埠
    def __initSerial(self):
        # 準備讀取arduino的序列埠
        try:
            self.__serial = serial.Serial("/dev/ttyACM0", 9600)  # 建立serial序列埠連線，序列埠名稱固定抓/dev/tty*，限制只能接一組arduino
            # self.__serial = serial.Serial("COM3", 9600)  # 建立serial序列埠連線，序列埠名稱固定抓/dev/tty*，限制只能接一組arduino
        except:
            messagebox.showerror("未連接溫度接收器", "未連接溫度接收序列埠，請確認是否接上，按下確定後，系統將自動重新啟動。")
            os.system("sudo reboot")
            exit()

    # 初始化溫度文件，每次啟動程式將__deviceRootPath資料夾移除重新建立溫度計序號資料夾
    def __initTempFile(self):
        # 移除舊的溫度計序號資料夾，重新建立
        if os.path.exists(self.__deviceRootPath) is True:
            shutil.rmtree(self.__deviceRootPath, ignore_errors=True)

    # arduino serial監聽執行緒，每0.1秒不斷更新接收到的溫度值
    def __arduinoSerialListen(self):
        try:
            while True:
                # 每次讀取一行(會等到序列埠輸出換行字元才會拋回資料)，並不斷覆蓋到變數中
                data = self.__serial.readline()
                data = data.decode('utf-8').strip('\n').strip('\r')
                # 讀到StopClick，表示按下了停止警報按鈕，直接呼叫停止警報程序
                if data == "StopClick":
                    self.__buzzer.close()
                    time.sleep(0.1)
                    continue
                # 更新變數溫度值
                self.__serialData = data
                time.sleep(0.1)
        except:
            messagebox.showerror("序列埠中斷", "序列埠已中斷，請確認USB接頭，按下確定後，系統將自動重新啟動。")
            os.system("sudo reboot")
            exit()

    # 更新溫度值到指定的檔案(仿樹梅派對於w1 device溫度文件做法)
    def __updateTempFile(self):
        while True:
            # 判斷從序列埠接到資料，才開始寫入溫度文件動作
            if self.__serialData is None:
                time.sleep(0.1)
                continue
            # 開始寫入溫度文件動作(無法轉成json的資料，拋棄，通常會發生在第一次抓到不完整的資料列)
            try:
                dataArray = json.loads(self.__serialData)
            except:
                time.sleep(0.1)
                continue
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
            # 登記為初始化完成
            if self.__initSuccess is False:
                self.__initSuccess = True
            # 每秒執行一次
            time.sleep(1)
