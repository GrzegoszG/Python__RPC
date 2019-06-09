import mysql.connector

class DbManager:

    host = ""
    user = ""
    passwd=""
    database = ""
    mydb = mysql.connector.MySQLConnection()
    cursor = mysql.connector.cursor.MySQLCursor()
    lastresult = dict()

    def __init__(self, _host, _user, _passwd, _database):
        self.host = _host
        self.user = _user
        self.passwd = _passwd
        self.database = _database
        self.mydb = self.connect()
        self.cursor = self.mydb.cursor()
        self.lastresult = dict()

    def connect(self):
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
            )
        return conn
    
    def executesql(self, query):
        self.cursor.execute(query)

    def commit_changes(self):
        self.mydb.commit()

    def get_result(self):

        if self.cursor.getlastrowid() == 0:
            result = list()
        else:
            result = self.cursor.fetchall()
        d = list()
        counter = 0
        for x in self.cursor.column_names:
            d.append(str(x))
            counter = counter + 1
        
        self.lastresult = list()

        for r in result:
            counter = 0
            dic = dict()
            for x in d:
                dic[str(x)] = r[counter]
                counter = counter + 1
            self.lastresult.append(dic)
        

        return self.lastresult
