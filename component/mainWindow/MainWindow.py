# coding=UTF-8
import tkinter as tk
from utilset.ConfigUtil import ConfigUtil
from component.mainWindow.BannerPanel import BannerPanel
from component.mainWindow.TempPanel import TempPanel
from component.mainWindow.WindowStyle import WinStyle as style


# 主要視窗物件
class MainWindow():

    __configUtil = None
    __width = style.WinWidth
    __height = style.WinHeight
    __window = None
    __canvas = None

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
        self.__window.title("溫度監控(ver.0.1.0)-" + self.__configUtil.DeviceName + "(" + self.__configUtil.DeviceID + ")")
        self.__window.geometry("%dx%d" % (self.__width, self.__height))
        self.__window.minsize(self.__width, self.__height)
        self.__window.maxsize(self.__width, self.__height)
        self.__window.config(bg="black")
        self.__window.attributes("-toolwindow", True)
        self.__window.protocol("WM_DELETE_WINDOW", False)  # 不允許使用者離開視窗
        # 生成canvas畫布物件，並佈滿整個window，提供各版面繪製介面
        #self.__canvas = tk.Canvas(self.__window, bg=style.Color.Black)
        #self.__canvas.pack(fill=tk.BOTH, expand=1)
        # 載入功能列表
        BannerPanel({
            "mainWindow": self.__window,
            "deviceName": self.__configUtil.DeviceName
        })
        # 載入溫度監視版面
        # TempPanel(self.__window)
