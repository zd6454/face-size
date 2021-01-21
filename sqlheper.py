import pymysql

class sqlHelper(object):
    def __init__(self):
        #读配置文件
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='2000825xym', db='face', charset='utf8')
        self.cursor = self.conn.cursor()

    def get_list(self,sql,args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def get_one(self,sql,args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def modify(self,sql,args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def multiple_modify(self,sql,args):
        self.cursor.executemany(sql, args)
        self.conn.commit()

    def create(self,sql,args):
        self.cursor.execute(sql, args)
        self.conn.commit()
        return  self.cursor.lastrowid

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()



