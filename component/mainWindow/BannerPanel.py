# coding=UTF-8
import tkinter as tk
import threading
import time
from PIL import Image, ImageTk


# 標頭列表
class BannerPanel():

    __mainWindow = None
    __deviceName = None
    __bannerPanel = None
    __buttonPanel = None
    __timeLabel = None
    __quitButton = None
    __setupButton = None
    __saveButton = None
    # 與外界連結要做動的panel物件
    __tempViewPanel = None
    __tempSetupPanel = None
    # style 屬性
    __bannerHeight = 48
    __iconWH = (48, 48)

    # 初始化
    def __init__(self, para):
        # 讀取參數
        self.__loadParameter(para)
        # 生成Banner Panel
        self.__genBannerPanel()

    # 讀取參數值方法
    def __loadParameter(self, para):
        self.__mainWindow = para["mainWindow"]
        self.__deviceName = para["deviceName"]

    # 生成Banner Panel
    def __genBannerPanel(self):
        # 生成banner容器框架
        self.__bannerPanel = tk.Frame(self.__mainWindow)
        self.__bannerPanel.config(bg="black", height=self.__bannerHeight)
        self.__bannerPanel.config(highlightbackground="white", highlightthickness=1)  # 設定border
        self.__bannerPanel.pack(fill=tk.BOTH, side=tk.TOP)
        # 生成按鈕容器框架，避免按鈕在異動pack時，影響到其他UI組件
        self.__buttonPanel = tk.Frame(self.__bannerPanel)
        self.__buttonPanel.pack(side=tk.RIGHT)
        # 生成離開按鈕
        self.__quitButton = self.__genButton({
            "IconPath": "./resource/quit.png",
            "event": self.__quitEvent
        })
        self.__quitButton.pack(side=tk.RIGHT)
        # 生成設定按鈕
        self.__setupButton = self.__genButton({
            "IconPath": "./resource/setup.png",
            "event": self.__setupEvent
        })
        self.__setupButton.pack(side=tk.RIGHT)
        # 生成存檔按鈕
        self.__saveButton = self.__genButton({
            "IconPath": "./resource/save.png",
            "event": self.__saveEvent
        })
        # 生成Title訊息
        self.__genTitle()
        # 生成時間訊息
        self.__genTime()

    # 生成按鈕
    def __genButton(self, para):
        # 讀取按鈕相關屬性
        iconPath = para["IconPath"]
        event = para["event"]
        # 讀取按鈕的icon
        loadIcon = Image.open(iconPath).resize(self.__iconWH, Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(loadIcon)
        # 生成按鈕
        button = tk.Button(self.__buttonPanel, image=icon, relief=tk.SOLID, command=event)
        button.config(bg="black", activebackground="gray")
        button.icon = icon
        return button

    # 生成Banner訊息文字
    def __genTitle(self):
        title = tk.Label(self.__bannerPanel)
        title.config(text=self.__deviceName, fg="white", bg="black", font=("NotoSansTC-Medium", 24))
        title.pack(side=tk.LEFT)

    # 生成時間訊息
    def __genTime(self):
        self.__timeLabel = tk.Label(self.__bannerPanel)
        self.__timeLabel.config(fg="white", bg="black", font=("NotoSansTC-Medium", 10))
        self.__timeLabel.pack(side=tk.RIGHT, anchor=tk.E)
        # 建立執行緒，用以更新時間
        task = threading.Thread(target=self.__renewTime)
        task.setDaemon(True)
        task.start()

    # 更新時間方法
    def __renewTime(self):
        while True:
            now = time.strftime("%Y/%m/%d\n%H:%M:%S", time.localtime())
            self.__timeLabel.config(text=now)
            time.sleep(1)

    # 離開按鈕事件
    def __quitEvent(self):
        # 關閉整個程式
        self.__mainWindow.destroy()
        self.__mainWindow = None
        exit()

    # 設定按鈕事件
    def __setupEvent(self):
        self.__setupButton.pack_forget()  # 關閉設定按鈕
        self.__saveButton.pack(side=tk.RIGHT)  # 開啟存檔按鈕
        self.__tempViewPanel.hide()  # 隱藏溫度檢視面板
        self.__tempSetupPanel.show()  # 開啟溫度設定面板

    # 存檔按鈕事件
    def __saveEvent(self):
        if self.__tempSetupPanel.save() is False:
            return
        self.__saveButton.pack_forget()  # 關閉存檔按鈕
        self.__setupButton.pack(side=tk.RIGHT)  # 開啟設定按鈕
        self.__tempSetupPanel.hide()  # 隱藏溫度設定面板
        self.__tempViewPanel.show()  # 開啟溫度檢視面板

    # 提供外界呼叫，設定連結「溫度檢視」版面與「溫度設定」版面，以利設定按鈕與存檔按鈕切換做動
    def setPanelFrame(self, para):
        self.__tempViewPanel = para["tempViewPanel"]
        self.__tempSetupPanel = para["tempSetupPanel"]
