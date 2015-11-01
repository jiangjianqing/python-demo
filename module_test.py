#!/usr/bin/python
# -*- coding: UTF-8 -*-

Money = 2000
def addmoney(a=1):
	#函数内引用全局变量
	print('测试变量作用域：')
	global Money
	print Money
	Money = Money + 1
	print Money

