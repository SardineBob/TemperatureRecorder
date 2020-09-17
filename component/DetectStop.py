import RPi.GPIO as GPIO


# 偵測實體按鈕按下的事件，用以關閉溫度異常警示語音
class DetectStop():

    __buzzer = None
    __stopPin = 20

    # 初始化，主要用來觸發警報器的停止事件
    def __init__(self, buzzer):
        self.__buzzer = buzzer
        # 設定GPIO相關參數
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.__stopPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.__stopPin, GPIO.RISING, callback=self.__stopEvent, bouncetime=500)

    # 當停止警報按鈕被下時，要執行的動作
    def __stopEvent(self, channel):
        self.__buzzer.close()