
import glob


# 溫度模組，this class for 1-Wire Interface for Raspberry Pi (Ex.DS18B20 Module)
class Temperature():

    __devicesPath = None
    __devicesFloder = None
    __devicesFile = None

    # 初始化，主要是定義一些路徑
    def __init__(self):
        #self.__devicesPath = "D://13.PythonProject/sys/bus/w1/devices/"
        self.__devicesPath = "/sys/bus/w1/devices/"
        self.__devicesFloder = glob.glob(self.__devicesPath + '28*')[0]
        self.__devicesFile = self.__devicesFloder + '/w1_slave'

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
