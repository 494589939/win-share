#!/usr/bin/python3
# ! conding = 'UTF-8'
# 文件名：server.py
from ast import literal_eval
import socket
from os import popen
from threading import Thread


# 添加授权重点函数：获取输入的文本打印到下面的文本框,需要导入END函数
def submit_grant(ls_dir, perm, rec, user_dates):
    for user in user_dates:
        cmd = r'Icacls "{dir}" /grant:r {user}:{perm} {rec}'.format(dir=ls_dir, user=user, perm=perm, rec=rec)
        print(cmd)
        res = popen(cmd)  # 调用popen命令打开一个管道相当于grep
        output_str = res.read()  # 获得输出字符串

    cmd2 = r'Icacls "{dir}" '.format(dir=ls_dir)
    res2 = popen(cmd2)
    output_str2 = res2.read()  # 获得输出字符串
    output_str3 = output_str + "授权清单如下：\n" + output_str2
    return output_str3


# 删除授权
def submit_remove(ls_dir, perm, rec, user_dates):
    for user in user_dates:
        cmd = r'Icacls "{dir}" /remove:g {user} {rec}'.format(dir=ls_dir, user=user, rec=rec)
        print(cmd)
        res = popen(cmd)  # 调用popen命令打开一个管道相当于grep
        output_str = res.read()  # 获得输出字符串

    cmd2 = r'Icacls "{dir}"'.format(dir=ls_dir)
    res2 = popen(cmd2)
    output_str2 = res2.read()  # 获得输出字符串
    output_str3 = output_str + "授权清单如下：\n" + output_str2
    return output_str3


# 查询授权信息
def query_grant(ls_dir, perm=None, rec=None, user_dates=None):
    cmd = r'Icacls "{ls_dir}" '.format(ls_dir=ls_dir)
    print(cmd)
    res = popen(cmd)  # 调用popen命令打开一个管道相当于grep
    output_str = res.read()  # 获得输出字符串
    return output_str


# 强制获取文件夹下面所有文件管理员授权
def force_grant(ls_dir, perm=None, rec=None, user_dates=None):
    cmd = r'takeown /f "{dir}" /r'.format(dir=ls_dir)
    res = popen(cmd)  # 调用popen命令打开一个管道相当于grep
    output_str = res.read()  # 获得输出字符串
    return output_str


# 备份文件夹授权
def backup_grant(ls_dir, perm=None, rec=None, user_dates=None):
    cmd = r'icacls "{dir}" /save "{dir}"\AclFile /T'.format(dir=ls_dir)
    res = popen(cmd)  # 调用popen命令打开一个管道相当于grep
    output_str = res.read()  # 获得输出字符串
    return output_str


# 查看文件夹
def ll_dir(ls_dir, perm=None, rec=None, user_dates=None):
    cmd = r'dir "{dir}" '.format(dir=ls_dir)
    popen(cmd)  # 调用popen命令打开一个管道相当于grep
    res = popen(cmd)  # 调用popen命令打开一个管道相当于grep
    output_str = res.read()  # 获得输出字符串
    return output_str


# 新建文件夹
def mk_dir(ls_dir, perm=None, rec=None, user_dates=None):
    cmd = r'md "{dir}" '.format(dir=ls_dir)
    popen(cmd)  # 调用popen命令打开一个管道相当于grep
    return "新建文件夹完成"


# 删除文件夹
def rd_dir(ls_dir, perm=None, rec=None, user_dates=None):
    cmd = r'rd /S /Q "{dir}" '.format(dir=ls_dir)
    popen(cmd)  # 调用popen命令打开一个管道相当于grep
    return "删除文件夹完成"


# 设置套接字
def socket_server():
    # 创建 socket 对象
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    # 获取本地主机名
    host = socket.gethostname()

    port = 9999

    # 绑定端口号
    serversocket.bind((host, port))

    # 设置最大连接数，超过后排队
    serversocket.listen(5)

    while True:
        # 建立客户端连接
        clientsocket, addr = serversocket.accept()

        # 接收数据
        client_data = clientsocket.recv(1024).decode('utf-8').split(';')
        print('接收到客户端的数据>>>', client_data)

        # 确定函数名
        func = client_data[0]
        # 确定客户端数据
        ls_dir = client_data[1]
        perm = client_data[2]
        rec = client_data[3]
        # 通过 literal_eval 这个函数，将str类型的列表转换成类型为list的真正的列表类型
        user_dates = literal_eval(client_data[4])

        # 发送数据 使用eval函数名的字符串调用函数
        send_data = eval(func)(ls_dir, perm, rec, user_dates)

        clientsocket.sendall(send_data.encode('utf-8'))
        print('发送给客户端的数据>>>', send_data)

        clientsocket.close()


if __name__ == '__main__':
    try:
        server_th = Thread(target=socket_server())
        # 设置线程为守护线程，防止退出主线程时，子线程仍在运行
        server_th.setDaemon(True)
        # 新线程启动
        server_th.start()
    except Exception as e:
        print("%s，重新尝试！" % e)
