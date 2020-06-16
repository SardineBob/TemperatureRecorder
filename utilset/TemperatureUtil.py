import os
from datetime import datetime
from utilset.SqlLiteUtil import SqlLiteUtil


# 將取到的溫度紀錄在DB
# 每天的溫度紀錄，會集中在同一個sqlLite db 檔案，也就是每天都會開不同db檔案存放溫度紀錄
class TemperatureUtil():

    __dbFilePath = None
    __sqlLiteUtil = None

    def __init__(self):
        self.__sqlLiteUtil = SqlLiteUtil()

    # 將溫度寫入DB
    def writeTemperature(self, temperature):
        # 先檢查dbfile是否存在
        self.__checkDB()
        # 將溫度insert到DB
        self.__insertTemperature({'temperature': temperature})

    # 檢查今天日期的DB是否已產生
    def __checkDB(self):
        # 取得今天db檔案路徑
        today = datetime.now().strftime('%Y%m%d')
        dbPath, dbFile = self.__getDBFilePath(today)
        # 檢查路徑是否存在，不存在則建立
        if os.path.exists(dbPath) is False:
            os.makedirs(dbPath)
        # 檢查今天DB檔案是否存在，不存在則開啟
        self.__dbFilePath = os.path.join(dbPath, dbFile)
        if os.path.isfile(self.__dbFilePath) is False:
            self.__createDB()

    # 取得今天的db檔案路徑(today format is 20200101)
    def __getDBFilePath(self, today):
        # 路徑的組成規則是:dbfile/西元年/月/年月日.db
        path = os.path.join('dbfile', today[0:4], today[4:6])
        filename = today + '.db'
        return (path, filename)

    # 產生DB檔案
    def __createDB(self):
        command = "CREATE TABLE RecordList(\
            RecodeTime Text NOT NULL,\
            Temperature REAL NOT NULL,\
            PRIMARY KEY (RecodeTime)\
        )"
        # do create db
        self.__sqlLiteUtil.Execute(self.__dbFilePath, command, [])

    # insert溫度資料
    def __insertTemperature(self, para):
        # 取出相關Insert資料
        temperature = para['temperature']
        now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        # insert 指令
        command = " INSERT INTO RecordList VALUES (:recordTime, :temperature) "
        parameter = {
            'recordTime': now,
            'temperature': temperature
        }
        # do insert to db
        self.__sqlLiteUtil.Execute(self.__dbFilePath, command, parameter)

    # select溫度資料(目前for one day)
    def selectTemperature(self, date):
        dbPath, dbFile = self.__getDBFilePath(date)
        dbFilePath = os.path.join(dbPath, dbFile)
        # 檢查這個日期有沒有db file
        if os.path.isfile(dbFilePath) is False:
            return str(date) + "這個日期無溫度數據資料。"
        # select 指令
        command = "SELECT * FROM RecordList"
        # get data from db
        return self.__sqlLiteUtil.Execute(dbFilePath, command, [])
