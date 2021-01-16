# coding=UTF-8
import os
import tkinter as tk
import tkinter.font as tkFont
import threading
import time
from component.Temperature import Temperature
from component.Buzzer import Buzzer
from component.SystemIntegrate import SystemIntegrate
from component.ArduinoReader import ArduinoReader


# 溫度檢視面版
class TempPanel():

    __mainWindow = None
    __deviceID = None  # 這個設備經由設定賦予他的編號，會與後台整合平台識別有關
    __thermometers = []  # 多筆溫度計物件
    __tempLinkList = []  # 連結對應的溫度計物件與溫度顯示介面，供執行緒抓取溫度後，呈現於顯示介面
    __tempCaptureTime = None  # 擷取溫度頻率秒數
    __TempPanel = None
    __buzzer = None  # 警報器物件
    __systemIntegrate = None  # 系統整合介接物件
    __arduinoReader = None  # Arduino資料接收器

    # 初始化
    def __init__(self, para):
        # 生成警報器物件
        self.__buzzer = Buzzer()
        # 生成Arduino資料接收器
        self.__arduinoReader = ArduinoReader(self.__buzzer)
        # 讀取參數
        self.__loadParameter(para)
        # 生成Temp Panel
        self.__genTempPanel()
        # 建立執行緒，更新溫度數值
        self.__genRenewTempThread()

    # 讀取參數值方法
    def __loadParameter(self, para):
        self.__mainWindow = para["mainWindow"]
        self.__deviceID = para["deviceID"]
        self.__tempCaptureTime = para["tempCaptureTime"]
        # 根據溫度計支數設定，逐一實體化溫度物件
        thermometers = para["thermometers"]
        for item in thermometers:
            # 判斷實際硬體有連接才運作
            temperature = Temperature(item)
            if temperature.isLinkHardware() is True:
                self.__thermometers.append(temperature)
        # 判斷都沒有連接溫度計，則提示訊息至少需插入一支溫度計才可運作
        if len(self.__thermometers) <= 0:
            tk.messagebox.showerror("偵測不到溫度計", "請至少連接一支溫度計，並按下確定，系統將自動重新啟動，以擷取連接的溫度計訊號。")
            os.system("sudo reboot")
            exit()
        # 實體化系統整合物件
        self.__systemIntegrate = SystemIntegrate()

    # 生成Temp Panel
    def __genTempPanel(self):
        # 生成溫度面板的容器框架
        self.__TempPanel = tk.Frame(self.__mainWindow)
        self.__TempPanel.config(bg="black")
        self.show()
        # 根據連接的溫度計，逐一生成溫度計資訊面板
        for tempItem in self.__thermometers:
            self.__genTempInfoPanel(tempItem)

    # 生成溫度計面板
    def __genTempInfoPanel(self, tempEntity):
        # 生成溫度資訊的容器框架
        tempInfoPanel = tk.Frame(self.__TempPanel)
        tempInfoPanel.config(bg="black")
        tempInfoPanel.config(highlightbackground="white", highlightthickness=1)  # 設定border
        tempInfoPanel.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        # 生成溫度計編號與名稱
        self.__genTempTitle({
            "panel": tempInfoPanel,
            "tempID": tempEntity.getID(),
            "tempName": tempEntity.getName(),
            "tempSerial": tempEntity.getSerial(),
        })
        # 生成溫度資訊
        self.__genTempLabel({
            "panel": tempInfoPanel,
            "tempEntity": tempEntity
        })

    # 生成溫度計編號與名稱
    def __genTempTitle(self, para):
        panel = para["panel"]
        tempID = para["tempID"]
        tempName = para["tempName"]
        tempSerial = para["tempSerial"]
        # 生成溫度計標題
        tempTitle = tk.Label(panel)
        tempTitle.config(text=str(tempID) + "\n" + tempSerial + "\n" + tempName)
        tempTitle.config(fg="white", bg="black", font=("NotoSansTC-Medium", 16))
        tempTitle.pack(fill=tk.BOTH, side=tk.TOP)

    # 生成溫度資訊
    def __genTempLabel(self, para):
        panel = para["panel"]
        tempEntity = para["tempEntity"]
        # 生成溫度計溫度顯示資訊
        tempLabel = tk.Label(panel)
        tempLabel.config(fg="white", bg="black", font=("NotoSansTC-Medium", 40))
        tempLabel.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)
        # 連結溫度資訊界面與溫度計物件
        self.__tempLinkList.append({
            "label": tempLabel,
            "entity": tempEntity
        })

    # 建立執行緒，更新溫度數值
    def __genRenewTempThread(self):
        task = threading.Thread(target=self.__renewTemp)
        task.setDaemon(True)
        task.start()

    # 每秒更新螢幕上的溫度，累積到設定秒數，才將溫度上傳整合平台
    def __renewTemp(self):
        postTempCount = 0 # 累積要上傳平台的秒數
        isAllCheckOK = True # 所有溫度計溫度是否均正常，只要一支不正常，則發送警報訊息給外掛警報器(保全器材第七迴路)
        while True:
            tempCollect = []
            for item in self.__tempLinkList:
                tempLabel = item["label"]
                tempEntity = item["entity"]
                # 讀取溫度
                temp = tempEntity.getTemperature()
                # 寫入資料庫
                tempEntity.writeTemperature(temp)
                # 收集溫度，準備發布溫度到雲端後台
                # 若收到溫度-999，表示接收不到溫度計數值，這邊根據需求，就不上傳平台
                if postTempCount >= self.__tempCaptureTime:
                    if temp > -999 :
                        tempCollect.append({
                            'deviceID': self.__deviceID,
                            'tempID': tempEntity.getID(),
                            'temp': temp
                        })
                # 呈現畫面
                tempLabel.config(text=str(round(temp, 1)) + "℃")
                # 檢查溫度是否超出正常範圍，超出範圍則字體紅色並語音警示
                isCheckOK = tempEntity.checkTemperature(temp)
                if isCheckOK is False:
                    self.__buzzer.trigger(tempLabel)
                isAllCheckOK = isAllCheckOK and isCheckOK
            # 若溫度超過，通知Serial發出警報，直到溫度恢復才關閉
            self.__arduinoReader.AlertToSerial(not isAllCheckOK)
            isAllCheckOK = True # 恢復預設值，下次AND邏輯閘才會是我要抓出的某一筆超過就警報
            # 發布溫度到雲端後台
            if postTempCount >= self.__tempCaptureTime:
                self.__systemIntegrate.postTemp(tempCollect)
                postTempCount = 0
            # 累計秒數，累積到設定秒數即上傳平台
            postTempCount = postTempCount+1
            # 每秒擷取溫度
            time.sleep(1)

    # 提供外界呼叫，開啟這個panel的方法
    def show(self):
        self.__TempPanel.pack(fill=tk.BOTH, expand=True)

    # 提供外界呼叫，隱藏這個panel的方法
    def hide(self):
        self.__TempPanel.pack_forget()
