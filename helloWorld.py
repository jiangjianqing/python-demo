#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import calendar
import time
import module_test
import os

from module_test import addmoney
from myclass import MyClass

sys.stdout.write("fole测试")

print "你好hello world!!!!!!!!!!!!!!!!",1!=2

def printcalenar():
	cal = calendar.month(2008, 1)
	print "Here is the calendar:"
	print cal

def printtime():
	localtime = time.asctime(time.localtime(time.time()))
	print "Local current time :", localtime

printcalenar()
printtime()


# 可写函数说明
def changeme( list ,age=1):
	"修改传入的列表"
	mylist.append([1,2,3,4])
	print "函数内取值: ", mylist
	print "age=",age
	return

# 调用changeme函数
mylist = [10,20,30]
changeme(list=mylist,age=3)
print "函数外取值: ", mylist


#dir()的参数必须是用import 引入的模块
content = dir(module_test)
print content

#可以通过module.funcname的方式调用模块中的函数或变量
module_test.addmoney()

#用from。。。import。。。引入的函数可以直接调用
addmoney()

print '当前目录：',os.getcwd()

#类实例化
obj=MyClass()
obj.readStr()
obj.writeStrToFile()


