#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import pexpect
import tarfile
import sys #用于获取命令行参数

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
    def checkout(self, repo_name, temp_dir):
        #targetdir = self.generatetempdirname()

        checkout_dir = temp_dir + "/" + repo_name
        tarFileName = "{repo_path}.tar.gz".format(repo_path=checkout_dir)
        # 字符串格式化范例
        # cmd = "svn checkout --username=%s --password=%s https://127.0.0.1:8443/svn/app" % (self.username, self.password)
        cmd = "svn checkout --username={username} --password={password} https://127.0.0.1:8443/svn/{repo}  {target}"\
            .format(username=self.username, password=self.password, repo=repo_name, target=checkout_dir)

        # 用os.system会出现错误：svn: E230001: Server SSL certificate verification failed:
        # certificate issued for a different hostname, issuer is not trusted
        #ret = os.system(cmd)

        child = pexpect.spawn(cmd)
        child.expect("\(R\)eject, accept \(t\)emporarily or accept \(p\)ermanently\? ", timeout=10)
        child.sendline("t\r\n")
        # 发送命令后必须等待结束
        child.wait()

        self.compressTempDir(tarFileName, checkout_dir)
        # 删除目录
        self.removeTempDir(checkout_dir)
        #self.removeTempDir("test.tar.gz")

        return tarFileName

    # 压缩指定目录
    def compressTempDir(self, output_filename, source_dir):
        # 一次性打包整个根目录。空子目录会被打包。
        # 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
            tar.close()

        # 逐个添加文件打包，未打包空子目录。可过滤文件。
        # 如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
        # 在后期的版本中需要对文件进行过滤，比如.svn文件夹就不应该被压缩
        '''
        tar = tarfile.open(output_filename, "w:gz")
        for root, dir, files in os.walk(source_dir):
            for file in files:
                pathfile = os.path.join(root, file)
                tar.add(pathfile)
        tar.close()
        '''

#   删除指定目录
    def removeTempDir(self, target_dir):
        os.system("test -e {target} && rm -rf {target} ".format(target=target_dir))

test1 = svnprovider(username="tester", password="tester")
username = "tester"
password = "tester"

#将用户名与密码保存在命令中，可以避免命令行交互
#svn_cmd = "svn checkout --username=tester --password=tester https://127.0.0.1:8443/svn/app ./svntest";

svn_cmd = "svn checkout --username=tester  https://127.0.0.1:8443/svn/app ./svntest"


def checkout(repo_name, temp_dir):
    return test1.checkout(repo_name, temp_dir)

if __name__ == "__main__":
    home_dir = os.path.expandvars('$HOME')
    if len(sys.argv)<2:
        print("参数格式错误")
        exit(1)
    repo_name = sys.argv[1]
    temp_dir = sys.argv[2]

    print("repo = {repo_name}".format(repo_name = repo_name))
    result = checkout(repo_name, "{home}".format(home=temp_dir))
    print(result)
    #test1.checkout("test")

    '''
    child = pexpect.spawn(svn_cmd)

    child.expect("ermanently\?", timeout=10)
    child.sendline("t\r")
    child.expect("password for 'tester':", timeout=10)
    child.sendline(password+"\r\n")

    child.expect("store password unencrypted (yes/no)?", timeout=10)
    #print(child.before)

    '''