#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta

class EmployeeDB:
	DB_NAME="employee"
	TABLES = {}

	def __init__(self):
		self.TABLES['employees'] = (
	    "CREATE TABLE employees ("
	    "  emp_no int(11) NOT NULL AUTO_INCREMENT,"
	    "  birth_date date NOT NULL,"
	    "  first_name varchar(14) NOT NULL,"
	    "  last_name varchar(16) NOT NULL,"
	    "  gender enum('M','F') NOT NULL,"
	    "  hire_date date NOT NULL,"
	    "  PRIMARY KEY (emp_no)"
	    ") ENGINE=InnoDB")

		self.TABLES['departments'] = (
	    "CREATE TABLE departments ("
	    "  dept_no char(4) NOT NULL,"
	    "  dept_name varchar(40) NOT NULL,"
	    "  PRIMARY KEY (dept_no), UNIQUE KEY dept_name (dept_name)"
	    ") ENGINE=InnoDB")

		try:
			#连接时不指定数据库的方式，可以通过cnx.database = DB_NAME这样的方式设定目标数据库
			self.cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1')
			cursor = self.cnx.cursor()
			self.cnx.database = self.DB_NAME
			print("连接数据库成功！")
			self.create_tables(cursor)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_BAD_DB_ERROR:
				self.create_db(cursor)
				print("创建数据库成功！")
				self.create_tables(cursor)
			else:
				print("连接数据库出错：{}".format(err))
				exit(1)
		else:
			cursor.close()

	def __del__(self):
		self.cnx.close()

	#创建数据库
	def create_db(self, cursor):
		try:
			cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.DB_NAME))
		except mysql.connector.Error as err:
			print("Failed creating database:{}".format(err))
			exit(1)

	#遍历TABLES并创建表
	def create_tables(self, cursor):
		for name, ddl in self.TABLES.iteritems():
			try:
				print("Creating table {}: ".format(name))
				cursor.execute(ddl)
			except mysql.connector.Error as err:
				if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
					print("already exists.")
				else:
					print(err.msg)
			else:
				print("ok")

	def test_insert_data(self):
		add_employee="INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date) VALUES (%s, %s, %s, %s, %s)"

		add_employee2="INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date) VALUES (%(first_name)s, %(last_name)s, %s(hire_date), %(gender)s, %(birth_date)s)"
		# Insert salary information

		tomorrow = datetime.now().date() + timedelta(days=1)
		data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

		data_employee2 = {
			'first_name': 'dict_abc',
			'last_name': 'dict_def',
			'hire_date': datetime.now().date() + timedelta(days=1),
			'gender': 'F',
			'birth_date': date(1978, 1, 1)
		}

		try:
			cursor = self.cnx.cursor()
			cursor.execute(add_employee, data_employee)
			emp_no = cursor.lastrowid
			print("最后插入的employee_id={}".format(emp_no))
			#使用dict方式作为参数在python2.7下没有成功
			#cursor.execute(add_employee2, data_employee2)
			self.cnx.commit()

		except BaseException as err:
			print('test_insert_data 发生错误：'.format(err))
			self.cnx.rollback()
		else:
			cursor.close()

	def test_query_data(self):
		query = ("""SELECT first_name, last_name, hire_date FROM employees
		         WHERE hire_date BETWEEN %s AND %s""")
		hire_start = date(1975, 1, 1)
		hire_end = date(2019, 12, 31)
		try:
			cursor = self.cnx.cursor()
			cursor.execute(query, (hire_start, hire_end))
			for (first_name, last_name, hire_date) in cursor:
				print("{}, {} was hired on {:%d %b %Y}".format(
					last_name, first_name, hire_date))
		except mysql.connector.Error as err:
			print("test_query_data occur error:".format(err))
		else:
			cursor.close()

