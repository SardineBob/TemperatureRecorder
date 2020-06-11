import time
from utilset.ConfigUtil import ConfigUtil
from component.Temperature import Temperature
from component.TemperatureWriter import TemperatureWriter

# 取得設定檔的值
TempCaptureTime = ConfigUtil().TempCaptureTime
# 開始無盡的根據設定循環秒數去擷取溫度數據並寫到SQLLite
active = True
temperature = Temperature()  # 溫度擷取物件
temperatureWriter = TemperatureWriter()  # 溫度紀錄物件
print('開始紀錄溫度(每' + str(TempCaptureTime) + '秒)')
try:
    while active:
        temp = temperature.getTemperature()
        temperatureWriter.writeTemperature(temp)
        print('目前溫度：' + str(temp))
        time.sleep(TempCaptureTime)
except KeyboardInterrupt:
    active = False

print('停止紀錄溫度')
