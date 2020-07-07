import os
from utilset.TemperatureUtil import TemperatureUtil
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_SSD1306


# OLED模組，this class for I2C Interface OLED Module for Raspberry Pi (Ex.SSD1315 Module)
class OLEDPrinter():

    __width = None
    __height = None
    __image = None
    __imageFont = None
    __imageDraw = None
    __fontTTCPath = './resource/mingliu.ttc'
    __display = None

    # 初始化，定義一些參數
    def __init__(self):
        # 準備輸出OLED display的物件
        self.__display = Adafruit_SSD1306.SSD1306_128_64(rst=None)
        self.__display.begin()
        self.__display.clear()
        self.__display.display()
        # 設定OLED Display螢幕長寬
        self.__width = self.__display.width
        self.__height = self.__display.height
        # 準備好繪圖相關的物件
        self.__image = Image.new('1', (self.__width, self.__height))
        #self.__imageFont = ImageFont.load_default()
        self.__imageFont = ImageFont.truetype(
            self.__fontTTCPath, encoding="UTF-8")
        self.__imageDraw = ImageDraw.Draw(self.__image)

    # 將溫度顯示在OLED螢幕上，最多三組溫度數值
    def print(self, tempCollect):
        # clear OLED Display
        self.__display.clear()
        self.__display.display()
        # draw Info.
        self.__draw(tempCollect)
        # print to OLED display
        self.__display.image(self.__image)
        self.__display.display()
        # self.__image.save("D:/test.jpg")

    # 繪製呈現在OLED螢幕上的影像
    def __draw(self, tempCollect):
        # clear image
        self.__imageDraw((0, 0, self.__width, self.__height), fill=0)
        # 根據連接的溫控棒數量，決定一格的高多少
        tempCnt = len(tempCollect)
        gridHeight = self.__height / tempCnt
        # draw Info. print to OLED
        for item in tempCollect:
            idx = tempCollect.index(item)
            y = idx * gridHeight
            (name, temp) = item
            # line
            if y > 0:
                lineLocate = [(0, y), (self.__width, y)]
                self.__imageDraw.line(lineLocate, fill=255, width=1)
            # text
            textLocate = (10, y + (gridHeight/4))
            text = name + ": " + str(temp)
            self.__imageDraw.text(
                textLocate, text, font=self.__imageFont, fill=255)
