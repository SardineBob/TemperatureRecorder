# coding=UTF-8
import os
from component.mainWindow.MainWindow import MainWindow

# 開啟溫度監控顯示視窗
try:
    MainWindow()
except Exception as err:
    print(err)
finally:
    print('reboot...')
    os.system("sudo reboot")
