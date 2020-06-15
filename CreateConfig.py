# coding=UTF-8
import configparser
import json

filePath = 'config.ini'
config = configparser.ConfigParser()

# 產生系統設定參數
config['SystemConfig'] = {
    'TempCaptureTime': json.dumps(5),  # 擷取溫度循環時間，每N秒，讀取溫度，並寫入溫度紀錄
}

# 寫入設定檔
with open('config.ini', 'w', encoding='UTF8') as configFile:
    config.write(configFile)
