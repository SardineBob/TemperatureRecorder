# coding=UTF-8
import tkinter as tk
import platform
from utilset.ConfigUtil import ConfigUtil
from component.mainWindow.BannerPanel import BannerPanel
from component.mainWindow.TempPanel import TempPanel
from component.mainWindow.TempSetupPanel import TempSetupPanel
from component.WebAPI import WebAPI


# 主要視窗物件
class MainWindow():

    __configUtil = None
    __width = 480
    __height = 320
    __window = None
    __bannerPanel = None
    __tempViewPanel = None
    __tempSetupPanel = None

    # 初始化

    def __init__(self):
        # 讀取設定檔
        self.__configUtil = ConfigUtil()
        # 載入視窗物件
        self.__loadWindow()
        # 啟動主視窗畫面
        self.__window.mainloop()

    # 載入視窗物件
    def __loadWindow(self):
        # 設定主視窗相關的屬性參數
        self.__window = tk.Tk()
        self.__window.title("溫度監控(ver.1.0.0)-" + self.__configUtil.DeviceName + "(" + self.__configUtil.DeviceID + ")")
        self.__width = self.__window.winfo_screenwidth()
        self.__height = self.__window.winfo_screenheight()
        self.__window.geometry("%dx%d" % (self.__width, self.__height))
        self.__window.minsize(self.__width, self.__height)
        self.__window.maxsize(self.__width, self.__height)
        self.__window.config(bg="black")
        self.__window.protocol("WM_DELETE_WINDOW", False)  # 不允許使用者離開視窗
        # 判斷作業系統環境，Window則該程式屬性指定為toolwindow，反之指定為fullscreen
        if platform.system() is "Windows":
            self.__window.attributes("-toolwindow", True)  # in window
        else:
            self.__window.attributes("-fullscreen", True)  # in raspberrypi
        # 載入功能列表
        self.__bannerPanel = BannerPanel({
            "mainWindow": self.__window,
            "deviceName": self.__configUtil.DeviceName
        })
        # 載入溫度檢視版面
        self.__tempViewPanel = TempPanel({
            "mainWindow": self.__window,
            "deviceID": self.__configUtil.DeviceID,
            "tempCaptureTime": self.__configUtil.TempCaptureTime,
            "thermometers": self.__configUtil.Thermometer
        })
        # 載入溫度設定版面
        self.__tempSetupPanel = TempSetupPanel({
            "mainWindow": self.__window,
            "configUtil": self.__configUtil,
        })
        # 將載入好的「溫度檢視」面板與「溫度設定」面板，連結到Banner物件，提供設定與存檔按鈕轉換連結對應
        self.__bannerPanel.setPanelFrame({
            "tempViewPanel": self.__tempViewPanel,
            "tempSetupPanel": self.__tempSetupPanel
        })
        # 建立WEB微服務
        WebAPI({'thermometers': self.__configUtil.Thermometer})
