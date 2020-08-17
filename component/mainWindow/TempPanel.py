# coding=UTF-8
import tkinter as tk
import tkinter.font as tkFont


# 功能列表
class TempPanel():

    __TempPanel = None
    __TempInfo = []

    # 初始化
    def __init__(self, mainWindow):
        # 建立一個容器，並建構在root主容器(也就是視窗)中，這個容器內的組件位置配置，就可以自行定義
        self.__TempPanel = tk.Frame(mainWindow)
        self.__TempPanel.configure(bg='#00ff00')
        # 這是基於root主容器的位置配置
        self.__TempPanel.grid(row=1, column=0, sticky='EWNS')
        # 根據連接的溫度計，配置版面(最多支援三支溫度計)
        self.__TempPanel.grid_columnconfigure(0, weight=1)
        self.__TempPanel.grid_columnconfigure(1, weight=1)
        self.__TempPanel.grid_columnconfigure(2, weight=1)
        self.__TempPanel.grid_rowconfigure(0, weight=1)
        # 溫度資訊版面
        TempInfo = tk.Frame(self.__TempPanel)
        TempInfo.configure(bg='#ff0000', highlightbackground='#000000', highlightthickness=1)
        TempInfo.grid(row=0, column=0, sticky='EWNS')
        # 溫度計編號
        tk.Label(TempInfo, text="溫度計編號：A01", font=("NotoSansTC-Medium", 12)).pack(fill=tk.BOTH)