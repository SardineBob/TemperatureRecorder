# coding=UTF-8
import time
from utilset.ConfigUtil import ConfigUtil
from component.Temperature import Temperature
from component.WebAPI import WebAPI
from component.OLEDPrinter import OLEDPrinter

# 取得設定檔的值
TempCaptureTime = ConfigUtil().TempCaptureTime
Thermometer = ConfigUtil().Thermometer
# 根據設定的溫控棒支數，逐一初始化
temperature = []
for item in Thermometer:
    temperature.append(Temperature(item))
oledPrinter = OLEDPrinter()
# 建立Web微服務
WebAPI({'temperature': temperature})
# 開始無盡的根據設定循環秒數去擷取溫度數據並寫到SQLLite
active = True
print('開始紀錄溫度(每' + str(TempCaptureTime) + '秒)')
try:
    while active:
        tempCollect = []
        for item in temperature:
            temp = item.getTemperature()
            tempCollect.append((item.getName(), temp))
            item.writeTemperature(temp)
            print('設備名稱：' + str(item.getName()) + '，目前溫度：' + str(temp))
        # 輸出到OLED螢幕
        oledPrinter.print(tempCollect)
        time.sleep(TempCaptureTime)
except KeyboardInterrupt:
    active = False

print('停止紀錄溫度')
