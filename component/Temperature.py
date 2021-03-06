import os
import platform
from utilset.TemperatureUtil import TemperatureUtil
from utilset.ConfigUtil import ConfigUtil


# 溫度模組，this class for 1-Wire Interface for Raspberry Pi (Ex.DS18B20 Module)
class Temperature():

    __devicesPath = None
    __id = None
    __name = None
    __serial = None
    __uplimit = None
    __lowlimit = None
    __devicesFolder = None
    __devicesFile = None
    __temperatureUtil = None

    # 初始化，主要是定義一些路徑
    def __init__(self, para):
        # 取得設定檔各項參數值
        self.__devicesPath = ConfigUtil().DeviceRootPath
        self.__id = para["id"]
        self.__name = para["name"]
        self.__serial = para["serial"]
        self.__uplimit = para["uplimit"]
        self.__lowlimit = para["lowlimit"]
        self.__devicesFloder = os.path.join(self.__devicesPath, self.__serial)
        self.__devicesFile = os.path.join(self.__devicesFloder, 'w1_slave')
        self.__temperatureUtil = TemperatureUtil()

    # 讀取w1介面寫到溫度的檔案，並回傳溫度數值
    def getTemperature(self):
        with open(self.__devicesFile, 'r') as file:
            # 檔案中只會固定有兩行，第一行device讀取溫度狀態，第二行是溫度，透過字串處理把資訊讀出來
            statusLine = file.readline()
            tempLine = file.readline()
            # 判斷如果沒有YES狀態，則回傳error temperature
            if 'YES' not in statusLine:
                return -999
            # 有YES狀態，就可以取得溫度數值
            temp = tempLine.split('t=')[1]
            temp = int(temp) / 1000  # 除1000就是真實的攝氏溫度

            return temp

    # 將溫度寫入DB中
    def writeTemperature(self, temperature):
        self.__temperatureUtil.writeTemperature({
            'id': self.__id,
            'name': self.__name,
            'temperature': temperature
        })

    # 檢查目前溫度，是否介於設定正常範圍內，以利出範圍出警報
    def checkTemperature(self, temperature):
        return not (temperature < self.__lowlimit or temperature > self.__uplimit)

    # 取得該溫控棒設定的代碼
    def getID(self):
        return self.__id

    # 取得該溫控棒設定的名稱
    def getName(self):
        return self.__name

    # 判斷設定的溫度計，實際硬體是否接上(檢查w1是否有該溫度檔案)
    def isLinkHardware(self):
        return os.path.isfile(self.__devicesFile)
