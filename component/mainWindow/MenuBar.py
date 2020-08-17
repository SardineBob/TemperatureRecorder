# coding=UTF-8
import tkinter as tk


# 功能列表
class MenuBar():

    __mainWindow = None
    __MenuBar = None

    # 初始化
    def __init__(self, mainWindow):
        self.__mainWindow = mainWindow
        # 建立一個容器，並建構在root主容器(也就是視窗)中，這個容器內的組件位置配置，就可以自行定義
        self.__MenuBar = tk.Frame(mainWindow)
        self.__MenuBar.configure(bg='#0000ff')
        # 這是基於root主容器的位置配置
        self.__MenuBar.grid(row=0, column=0, sticky='EWNS')
        # 生成離開按鈕
        tk.Button(self.__MenuBar, text="Exit", command=self.__quitEvent).pack(side=tk.RIGHT, anchor=tk.N, fill='y')

    # 離開按鈕事件
    def __quitEvent(self):
        self.__mainWindow.destroy()
        self.__mainWindow = None
        exit()