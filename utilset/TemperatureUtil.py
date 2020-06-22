import os
from datetime import datetime
from utilset.SqlLiteUtil import SqlLiteUtil


# 將讀取到的溫度紀錄在DB
# 每年的溫度紀錄，會集中在同一個sqlLite db 檔案，也就是每年都會開不同db檔案存放溫度紀錄
class TemperatureUtil():

    __dbPath = "dbfile"
    __dbFilePath = None
    __sqlLiteUtil = None

    def __init__(self):
        self.__sqlLiteUtil = SqlLiteUtil()

    # 將溫度寫入DB
    def writeTemperature(self, para):
        # 先檢查dbfile是否存在
        self.__checkDB()
        # 將溫度insert到DB
        self.__insertTemperature(para)

    # 檢查今年的DB是否已產生
    def __checkDB(self):
        # 取得今年db檔案路徑
        dbFile = datetime.now().strftime('%Y') + '.db'
        # 檢查路徑是否存在，不存在則建立
        if os.path.exists(self.__dbPath) is False:
            os.makedirs(self.__dbPath)
        # 檢查今天DB檔案是否存在，不存在則開啟
        self.__dbFilePath = os.path.join(self.__dbPath, dbFile)
        if os.path.isfile(self.__dbFilePath) is False:
            self.__createDB()

    # 產生DB檔案
    def __createDB(self):
        command = "CREATE TABLE RecordList(\
            ID INTEGER NOT NULL,\
            Name Text NOT NULL,\
            RecodeTime Text NOT NULL,\
            Temperature REAL NOT NULL,\
            PRIMARY KEY (ID, RecodeTime)\
        )"
        # do create db
        self.__sqlLiteUtil.Execute(self.__dbFilePath, command, [])

    # insert溫度資料
    def __insertTemperature(self, para):
        # 取出相關Insert資料
        id = para['id']
        name = para['name']
        temperature = para['temperature']
        now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        # insert 指令
        command = " INSERT INTO RecordList VALUES (:id, :name, :recordTime, :temperature) "
        parameter = {
            'id': id,
            'name': name,
            'recordTime': now,
            'temperature': temperature
        }
        # do insert to db
        self.__sqlLiteUtil.Execute(self.__dbFilePath, command, parameter)

    # select溫度資料(目前for one day)
    def selectTemperature(self, date):
        dbFile = datetime.now().strftime('%Y') + '.db'
        dbFilePath = os.path.join(self.__dbPath, dbFile)
        # 檢查這個日期有沒有db file
        if os.path.isfile(dbFilePath) is False:
            return str(date) + "這個日期無溫度數據資料。"
        # select 指令
        command = "SELECT * FROM RecordList"
        # get data from db
        return self.__sqlLiteUtil.Execute(dbFilePath, command, [])
