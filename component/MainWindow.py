# coding=UTF-8
import tkinter as tk


class MainWindow():

    __width = 480
    __height = 320
    __window = None

    # 初始化
    def __init__(self):
        # 載入視窗物件
        self.__loadWindow()
        # 啟動主視窗畫面
        self.__window.mainloop()

    # 載入視窗物件
    def __loadWindow(self):
        # 設定主視窗相關的屬性參數
        self.__window = tk.Tk()
        self.__window.title("溫度監控(ver.0.1.0)")
        self.__window.geometry("%dx%d" % (self.__width, self.__height))
        self.__window.minsize(self.__width, self.__height)
        self.__window.maxsize(self.__width, self.__height)
        self.__window.attributes("-toolwindow", True)
        self.__window.protocol("WM_DELETE_WINDOW", False)  # 不允許使用者離開視窗
        # 生成離開按鈕
        tk.Button(self.__window, text="Exit", command=self.__quitEvent).pack(anchor=tk.NE)

    # 離開按鈕事件
    def __quitEvent(self):
        self.__window.destroy()
        self.__window = None
        exit()
