# coding=UTF-8
import configparser
import json

filePath = 'config.ini'
config = configparser.ConfigParser()

# 產生系統設定參數
config['SystemConfig'] = {
    'DeviceID': json.dumps("0001", ensure_ascii=False),
    'DeviceName': json.dumps("墾丁分店", ensure_ascii=False),
    'TempCaptureTime': json.dumps(6),  # 擷取溫度循環時間，每N秒，讀取溫度，並寫入溫度紀錄
    'Thermometer': json.dumps([
        {'id': 1, 'name': '左邊冷凍櫃', 'serial': '28-041694bd1cff'},
        {'id': 2, 'name': '中間冷凍櫃', 'serial': '28-041694bd1cfg'},
        {'id': 3, 'name': '右邊冷凍櫃', 'serial': '28-041694bd1cfh'},
    ], ensure_ascii=False),  # 溫度計硬體設備序號與名稱
}

# 寫入設定檔
with open(filePath, 'w', encoding='UTF8') as configFile:
    config.write(configFile)
