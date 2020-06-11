import sqlite3


class SqlLiteUtil():

    # 執行SQL Lite指令
    def Execute(self, dbFile, sqlcommand, sqlparamter):
        with sqlite3.connect(dbFile) as conn:
            cur = conn.cursor()
            cur.execute(sqlcommand, sqlparamter)
            conn.commit()
            # 把結果轉為List<tuple>
            data = []
            for row in cur:
                data.append(row)
            return data
