# coding=UTF-8
import tkinter as tk
import threading
import time
from PIL import Image, ImageTk
from component.mainWindow.WindowStyle import WinStyle


# 標頭列表
class BannerPanel():

    __mainWindow = None
    __deviceName = None
    __bannerPanel = None
    __timeLabel = None
    __renewTimeTask = None
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
        # 生成離開按鈕
        self.__genButton({
            "IconPath": "./resource/quit.png",
            "event": self.__quitEvent
        })
        # 生成設定按鈕
        self.__genButton({
            "IconPath": "./resource/setup.png",
            "event": self.__test
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
        button = tk.Button(self.__bannerPanel, image=icon, relief=tk.SOLID, command=event)
        button.config(bg="black", activebackground="gray")
        button.icon = icon
        button.pack(side=tk.RIGHT)

    # 生成Banner訊息文字
    def __genTitle(self):
        title = tk.Label(self.__bannerPanel)
        title.config(text=self.__deviceName, fg="white", bg="black", font=("NotoSansTC-Medium", 24))
        title.pack(side=tk.LEFT)

    # 生成時間訊息
    def __genTime(self):
        self.__timeLabel = tk.Label(self.__bannerPanel)
        self.__timeLabel.config(fg="white", bg="black", font=("NotoSansTC-Medium", 10))
        self.__timeLabel.pack(side=tk.RIGHT, anchor=tk.N)
        # 建立執行緒，用以更新時間
        self.__renewTimeTask = threading.Thread(target=self.__renewTime)
        self.__renewTimeTask.setDaemon(True)
        self.__renewTimeTask.start()

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

    def __test(self):
        print('click')
