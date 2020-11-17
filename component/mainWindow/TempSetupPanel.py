# coding=UTF-8
import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import threading
import time
from PIL import Image, ImageTk


# 溫度檢視面版
class TempSetupPanel():

    __mainWindow = None
    __configUtil = None
    __tempSetupFrame = None
    __tempSetupList = []  # 透過物件組合對應設定檔物件以及版面物件

    # 初始化
    def __init__(self, para):
        # 讀取參數
        self.__loadParameter(para)
        # 生成溫度設定面板總成
        self.__genTempSetupFrame()

    # 讀取參數值方法
    def __loadParameter(self, para):
        self.__mainWindow = para["mainWindow"]
        self.__configUtil = para["configUtil"]

    # 生成溫度設定面板總成
    def __genTempSetupFrame(self):
        # 生成溫度設定總面板容器框架
        self.__tempSetupFrame = tk.Frame(self.__mainWindow)
        self.__tempSetupFrame.config(bg="black")
        # 根據連接的溫度計，逐一生成溫度計設定面版
        for tempItem in self.__configUtil.Thermometer:
            self.__genTempSetupPanel(tempItem)

    # 生成溫度設定面板
    def __genTempSetupPanel(self, tempEntity):
        # 生成溫度資訊的容器框架
        tempSetupPanel = tk.Frame(self.__tempSetupFrame)
        tempSetupPanel.config(bg="black")
        tempSetupPanel.config(highlightbackground="white", highlightthickness=1)  # 設定border
        tempSetupPanel.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        # 生成溫度計編號與名稱
        self.__genTempTitle({
            "panel": tempSetupPanel,
            "tempID": tempEntity["id"],
            "tempName": tempEntity["name"],
            "tempSerial": tempEntity["serial"],
        })
        # 生成溫度上限設定版面
        upLimitItem = self.__genTemplimitPanel({
            "panel": tempSetupPanel,
            "limitVal": tempEntity["uplimit"],
            "fontColor": "red"
        })
        # 生成溫度下限設定版面
        lowLimitItem = self.__genTemplimitPanel({
            "panel": tempSetupPanel,
            "limitVal": tempEntity["lowlimit"],
            "fontColor": "blue"
        })
        # 綁定設定檔物件與版面操作設定值結果
        self.__tempSetupList.append({
            "Thermometer": tempEntity,
            "upLimitItem": upLimitItem,
            "lowLimitItem": lowLimitItem
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
        tempTitle.config(fg="white", bg="black", font=("NotoSansTC-Medium", 14))
        tempTitle.pack(fill=tk.BOTH, side=tk.TOP)

    # 生成溫度上限/下限版面
    def __genTemplimitPanel(self, para):
        # 讀取參數
        panel = para["panel"]
        limitVal = para["limitVal"]
        fontColor = para["fontColor"]
        # 生成UI物件以及限度值變數組合物件
        item = {
            "label": None,
            "limitVal": limitVal
        }
        # 生成溫度計設定框架
        frame = tk.Frame(panel)
        frame.config(bg="black")
        frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        # 生成增加溫度按鈕
        self.__genUpLowButton({
            "iconPath": "./resource/up.png",
            "frame": frame,
            "clickEvent": lambda: self.__setupUpperEvent(item)
        })
        # 生成溫度計溫度顯示資訊
        templimitLabel = tk.Label(frame)
        templimitLabel.config(fg=fontColor, bg="black", font=("NotoSansTC-Medium", 30))
        templimitLabel.config(text=limitVal)
        templimitLabel.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        item["label"] = templimitLabel
        # 生成降低溫度按鈕
        self.__genUpLowButton({
            "iconPath": "./resource/down.png",
            "frame": frame,
            "clickEvent": lambda: self.__setupLowerEvent(item)
        })
        return item

    # 生成增加/降低溫度按鈕
    def __genUpLowButton(self, para):
        # 讀取參數
        iconPath = para["iconPath"]
        frame = para["frame"]
        clickEvent = para["clickEvent"]
        # 讀取增加圖示
        loadIcon = Image.open(iconPath).resize((40, 40), Image.ANTIALIAS)
        icon = ImageTk.PhotoImage(loadIcon)
        # 產生按鈕
        button = tk.Button(frame, image=icon, relief=tk.SOLID, command=clickEvent)
        button.config(bg="black", activebackground="gray")
        button.icon = icon
        button.pack(fill=tk.BOTH, side=tk.LEFT)

    # 提高溫度事件
    def __setupUpperEvent(self, item):
        # 讀取物件屬性
        label = item["label"]
        limitVal = item["limitVal"]
        # 判斷最高設定不超過125度
        if limitVal >= 125:
            return
        # 加1後，更新UI顯示
        limitVal = limitVal + 1
        label.config(text=limitVal)
        item["limitVal"] = limitVal

    # 降低溫度事件
    def __setupLowerEvent(self, item):
        # 讀取物件屬性
        label = item["label"]
        limitVal = item["limitVal"]
        # 判斷最低設定不超過-55度
        if limitVal <= -55:
            return
        # 加1後，更新UI顯示
        limitVal = limitVal - 1
        label.config(text=limitVal)
        item["limitVal"] = limitVal

    # 將新的設定值存檔
    def save(self):
        # 逐一取出設定檔物件與介面設定值，更新設定值後存檔
        for item in self.__tempSetupList:
            thermometer = item["Thermometer"]
            upLimitVal = item["upLimitItem"]["limitVal"]
            lowLimitVal = item["lowLimitItem"]["limitVal"]
            # 檢查上限不可以低於下限
            if lowLimitVal > upLimitVal:
                messagebox.showerror("error", "上限溫度不可低於下限溫度。")
                return False
            # 更新設定值至設定檔
            thermometer["uplimit"] = upLimitVal
            thermometer["lowlimit"] = lowLimitVal
        # 存檔
        self.__configUtil.save()
        messagebox.showinfo("info", "存檔成功，按下確定後，系統將自動重新啟動，以更新設定值。")
        os.system("sudo reboot")
        return True

    # 提供外界呼叫，開啟這個panel的方法
    def show(self):
        self.__tempSetupFrame.pack(fill=tk.BOTH, expand=True)

    # 提供外界呼叫，隱藏這個panel的方法
    def hide(self):
        self.__tempSetupFrame.pack_forget()
