# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta 
import pymysql.cursors;
import logging

config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'123456',
          'db':'test',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }
 
# Connect to the database
connection = pymysql.connect(**config)

# 获取明天的时间
tomorrow = datetime.now().date() + timedelta(days=1)

print(tomorrow)

# 执行sql查询语句
try:
    with connection.cursor() as cursor:
    	
# 执行sql语句，插入记录
        # sql = 'INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date) VALUES (%s, %s, %s, %s, %s)'
        # cursor.execute(sql, ('Robin', 'Zhyea', tomorrow, 'M', date(1989, 6, 14)));
    	# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
    	# connection.commit()

    	# sql = 'SELECT first_name, last_name, hire_date FROM employees WHERE hire_date BETWEEN %s AND %s'
        # cursor.execute(sql, (hire_start, hire_end))
        # 执行sql语句，进行查询
        sql = 'SELECT * FROM test1'
        cursor.execute(sql)
        # 获取查询结果
        result = cursor.fetchone()
        #获取指定数量的记录（不推荐，还是放在sql语句中比较好）
        #result = cursor.fetchmany(2)
        #获取全部记录
        #result = cursor.fetchall()
        print(result)
 
finally:
    connection.close();

# --------------------------------end ------------------------------------------------
class MySQLCommand(object):
    def __init__(self,host,port,user,passwd,db,table):
        self.host = host
        self.port = port
        self.user = user
        self.password = passwd
        self.db = db
        self.table = table

    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host,port=self.port,user=self.user,passwd=self.password,db=self.db,charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    def queryMysql(self):
        sql = "SELECT * FROM " + self.table

        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            print(row)

        except:
            print(sql + ' execute failed.')

    def insertMysql(self,id,name,sex):
        sql = "INSERT INTO " + self.table + " VALUES(" + id + "," + "'" + name + "'," + "'" + sex + "')"
        try:
            self.cursor.execute(sql)
        except:
            print("insert failed.")

    def updateMysqlSN(self,name,sex):
        sql = "UPDATE " + self.table + " SET sex='" + sex + "'" + " WHERE name='" + name + "'"
        print("update sn:" + sql)

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()


    def closeMysql(self):
        self.cursor.close()
        self.conn.close()