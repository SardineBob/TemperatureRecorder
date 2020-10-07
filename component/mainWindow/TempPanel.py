# coding=UTF-8
import tkinter as tk
import tkinter.font as tkFont
import threading
import time
from component.Temperature import Temperature
from component.Buzzer import Buzzer
from component.SystemIntegrate import SystemIntegrate
from component.DetectStop import DetectStop


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
    __detectStop = None  # 偵測GPIO按鈕停止警報物件

    # 初始化
    def __init__(self, para):
        # 讀取參數
        self.__loadParameter(para)
        # 生成警報器物件
        self.__buzzer = Buzzer()
        # 生成偵測停止按鈕物件
        self.__detectStop = DetectStop(self.__buzzer)
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
            tk.messagebox.showerror("偵測不到溫度計", "請至少連接一支溫度計方可運作。")
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
        # 生成溫度計標題
        tempTitle = tk.Label(panel)
        tempTitle.config(text=str(tempID) + "\n" + tempName, fg="white", bg="black", font=("NotoSansTC-Medium", 18))
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

    # 每到設定的頻率秒數，就更新溫度
    def __renewTemp(self):
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
                tempCollect.append({
                    'deviceID': self.__deviceID,
                    'tempID': tempEntity.getID(),
                    'temp': temp
                })
                # 呈現畫面
                tempLabel.config(text=str(int(temp)) + "℃")
                # 檢查溫度是否超出正常範圍，超出範圍則字體紅色並語音警示
                if tempEntity.checkTemperature(temp) is False:
                    self.__buzzer.trigger(tempLabel)
            # 發布溫度到雲端後台
            self.__systemIntegrate.postTemp(tempCollect)
            # 等待設定秒數，再行擷取溫度
            time.sleep(self.__tempCaptureTime)

    # 提供外界呼叫，開啟這個panel的方法
    def show(self):
        self.__TempPanel.pack(fill=tk.BOTH, expand=True)

    # 提供外界呼叫，隱藏這個panel的方法
    def hide(self):
        self.__TempPanel.pack_forget()
