#!/usr/bin/python
# -*- coding: UTF-8 -*-


class MyClass:#定义类范例


	def __init__(self):
		self.str = ''

	def __del__(self):
		class_name = self.__class__.__name__
		print class_name, "destroyed"

	def readStr(self):
		self.str = raw_input("Enter your input: ")
		print "Received input is : ", self.str

	def writeStrToFile(self):
		try:
			fo=open('/tmp/test','wb')
			fo.write(self.str)
		finally:
			fo.close()
