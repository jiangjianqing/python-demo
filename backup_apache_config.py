#!/usr/bin/python
# -*- coding: UTF-8 -*-
#本脚本用来备份apache的配置文件

import os
import time
import shutil
import re
import getpass

def createdir(dir_name):
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)

#根据用户名确定目录位置
#os.getlogin() 也可以达到效果,但在下面使用会出错，奇怪
#getpass.getuser()推荐使用
#os.getuid()==0可以判断是否root
backup_dir="{}/apache_config_backup".format(os.environ['HOME'])
#print backup_dir
apache_dir="/usr/local/apache2"
if not os.path.exists(apache_dir):
	print("确认是否已经安装apache，操作被终止！")
	exit(0)
current_backup_dir="{}/{}".format(backup_dir,time.strftime("%Y%m%d_%H%M%S", time.localtime()))

localtime = time.localtime(time.time())

createdir(backup_dir)
#createdir(current_backup_dir) #shutil.copytree会创建目录，所以这里可以屏蔽
memo_file_name="backup_memo"
i=0
for parent,dirnames,filenames in os.walk(backup_dir):
	i+=1
	if parent==backup_dir:
		for dirname in  dirnames:                       #输出文件夹信息
			memo_file="{}/{}/{}".format(backup_dir,dirname,memo_file_name)
			memo_info="[无备注]"
			if os.path.exists(memo_file):
				file_object = open(memo_file, 'r')
				memo_info=file_object.read()
				file_object.close()
			print "编号:{},dirname:{}\nmemo:{}".format(i,memo_file,memo_info)
			"""
			print "parent is:" + parent
			print  "dirname is" + dirname
			"""

"""
	for filename in filenames:                        #输出文件信息
		print "parent is:"+ parent
		print "filename is:" + filename
		print "the full name of the file is:" + os.path.join(parent,filename) #输出文件路径信息
"""
backup_memo = raw_input("请输入备注信息(input n 代表放弃): ")
if backup_memo=="":
	print("备注信息必须输入！！！！备份失败")
	exit(1)
matchObj=re.match(r'[nN]|[nN]o',backup_memo,re.M|re.I)
if matchObj:
	print("放弃备份")
	exit(0)

target_files=("conf","")
for item in target_files:
	if item=="":
		continue;
	target_item="{}/{}".format(apache_dir,item)
	print target_item
	if os.path.isfile(item)==True:
		pass
	else:
		shutil.copytree(target_item,current_backup_dir,False)
		if backup_memo!="":
			file_object = open('{}/{}'.format(current_backup_dir,'backup_memo'), 'w')
			file_object.write(backup_memo)
			file_object.close()

print("备份完成，目录为:{}".format(current_backup_dir))

