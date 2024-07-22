import pymysql
class master_flask_code:
    def __init__(self):
        self.user = 'root'
        self.password = ''
        self.host = 'localhost'
        self.database = 'python_farming_machinery'
    def select_direct_query(self, qry):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.database, charset='utf8')
        cursor = conn.cursor()
        cursor.execute(qry)
        data = cursor.fetchall()
        conn.close()
        return data
    def find_max_id(self,table):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.database,charset='utf8')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM "+table)
        data = cursor.fetchall()
        maxin = len(data)
        if maxin == 0:
            maxin = 1
        else:
            maxin += 1
        return maxin
    def insert_query(self,qry):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.database,charset='utf8')
        cursor = conn.cursor()
        result=cursor.execute(qry)
        conn.commit()
        conn.close()
        return result
    def select_login(self,qry):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.database,charset='utf8')
        cursor = conn.cursor()
        cursor.execute(qry)
        data = cursor.fetchall()
        check = len(data)
        if check == 0:
            return 'no'
        else:
            return 'yes'
    def select_single_colum(self,table,colum):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.database,charset='utf8')
        qry1=("select "+colum+"  from "+table)
        cursor = conn.cursor()
        cursor.execute(qry1)
        data = cursor.fetchall()
        return data

    def select_direct_query(self,qry):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.database,charset='utf8')
        cursor = conn.cursor()
        cursor.execute(qry)
        data = cursor.fetchall()
        return data




