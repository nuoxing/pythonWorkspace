import pymysql


class DbHandler():

    host = "192.168.200.100"
    user = "root"
    password = "123456"
    port = 3306
    db = "ipet"

    def __init__(self):
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port,db=self.db,charset="utf8")
        self.cursor = self.db.cursor()


    def insert(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        finally:
            self.db.close()
        pass


