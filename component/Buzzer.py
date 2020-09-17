import threading
import time
from playsound import playsound


# 警報器，當溫度超出正常範圍時觸發
class Buzzer():

    __labelList = []
    __labelShinyTask = None  # 警報進行中的執行緒，負責閃爍溫度字體
    __labelShinyActive = False
    __alertSoundTask = None  # 警報進行中的執行緒，負責不斷撥放警報語音
    __alertSoundActive = False
    __alertSoundPath = "./resource/alert.mp3"

    # 觸發警報，除了將傳進來的溫度Label物件字體變為紅白閃爍，同時也不斷撥放警報語音
    def trigger(self, label):
        # 判斷該Label物件是否存在，存在就不需要append到需處理清單
        if label in self.__labelList:
            return
        self.__labelList.append(label)
        # 判斷如果執行緒沒開啟，則建立字體閃爍的執行緒
        if self.__labelShinyTask is None:
            self.__labelShinyActive = True
            self.__labelShinyTask = threading.Thread(target=self.__labelShinyEvent)
            self.__labelShinyTask.setDaemon(True)
            self.__labelShinyTask.start()
        # 判斷如果執行緒沒開啟，則建立播放警報語音的執行緒
        if self.__alertSoundTask is None:
            self.__alertSoundActive = True
            self.__alertSoundTask = threading.Thread(target=self.__alertSoundEvent)
            self.__alertSoundTask.setDaemon(True)
            self.__alertSoundTask.start()

    # 關閉警報，字體顏色恢復，停止撥放語音，執行緒停止
    def close(self):
        # 判斷警報器沒有觸發，則不動作
        if self.__labelShinyTask is None:
            return
        # 恢復字體為白色
        for label in self.__labelList:
            label.config(fg="white")
        # 清空狀態與停止執行緒
        self.__labelList = []
        self.__labelShinyActive = False
        self.__alertSoundActive = False
        self.__labelShinyTask = None
        self.__alertSoundTask = None

    # 執行溫度字體閃爍動作
    def __labelShinyEvent(self):
        fgColor = ""
        while self.__labelShinyActive:
            fgColor = "white" if fgColor is "red" else "red"
            for label in self.__labelList:
                label.config(fg=fgColor)
            time.sleep(0.5)

    # 執行不斷撥放警報語音動作
    def __alertSoundEvent(self):
        while self.__alertSoundActive:
            playsound(self.__alertSoundPath)
            time.sleep(0.5)
