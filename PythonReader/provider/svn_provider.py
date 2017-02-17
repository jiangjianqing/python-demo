#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pexpect
import tarfile

class svnprovider(object):
    """docstring for classname"""
    def __init__(self, **kwargs):
        super(svnprovider, self).__init__()
        self.username = "tester"
        self.password = "tester"
        if "username" in kwargs:
            self.username = kwargs["username"]
        if "password" in kwargs:
            self.password = kwargs["password"]

    # 生成唯一的路径名称
    def generatetempdirname(self):
        return "./svntest"

    #将目标模块签出，需要参数：ip地址、端口、svn子地址、项目（模块）名称、分支（版本）名称
    def checkout(self):
        targetdir = self.generatetempdirname();
        # 字符串格式化范例
        # cmd = "svn checkout --username=%s --password=%s https://127.0.0.1:8443/svn/app" % (self.username, self.password)
        cmd = "svn checkout --username={username} --password={password} https://127.0.0.1:8443/svn/app  {target}"\
            .format(username=self.username, password=self.password, target=targetdir)

        # 用os.system会出现错误：svn: E230001: Server SSL certificate verification failed:
        # certificate issued for a different hostname, issuer is not trusted
        #ret = os.system(cmd)

        child = pexpect.spawn(cmd)
        child.expect("\(R\)eject, accept \(t\)emporarily or accept \(p\)ermanently\? ", timeout=10)
        child.sendline("t\r\n")
        # 发送命令后必须等待结束
        child.wait()

        self.compressTempDir("test.tar.gz", targetdir)
        # 删除目录
        self.removeTempDir(targetdir)
        self.removeTempDir("test.tar.gz")

    # 压缩指定目录
    def compressTempDir(self, output_filename, source_dir):
        # 一次性打包整个根目录。空子目录会被打包。
        # 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
            tar.close()

        # 逐个添加文件打包，未打包空子目录。可过滤文件。
        # 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
        '''
        tar = tarfile.open(output_filename, "w:gz")
        for root, dir, files in os.walk(source_dir):
            for file in files:
                pathfile = os.path.join(root, file)
                tar.add(pathfile)
        tar.close()
        '''

#   删除指定目录
    def removeTempDir(self, targetDir):
        os.system("test -e {target} && rm -rf {target} ".format(target=targetDir))





test1 = svnprovider(username="tester", password="tester")


username = "tester"
password = "tester"

#将用户名与密码保存在命令中，可以避免命令行交互
#svn_cmd = "svn checkout --username=tester --password=tester https://127.0.0.1:8443/svn/app ./svntest";

svn_cmd = "svn checkout --username=tester  https://127.0.0.1:8443/svn/app ./svntest"


if __name__ == "__main__":
    test1.checkout()

    '''
    child = pexpect.spawn(svn_cmd)

    child.expect("ermanently\?", timeout=10)
    child.sendline("t\r")
    child.expect("password for 'tester':", timeout=10)
    child.sendline(password+"\r\n")

    child.expect("store password unencrypted (yes/no)?", timeout=10)
    #print(child.before)

    '''