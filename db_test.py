#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql.connector

from EmployeeManager import EmployeeDB

from mysql.connector import errorcode

employeeDB=EmployeeDB()
employeeDB.test_insert_data()
employeeDB.test_query_data()

config = {
    'user': 'root',
    'password': '123',
    'host': '127.0.0.1',
    'database': 'test'
}

try:
    #cnx = mysql.connector.connect(**config)#使用dict的方式try 语句不会捕获错误
    cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='test')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print("other error:{}".format(err))
else:
    cnx.close()

