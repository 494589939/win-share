#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
from threading import Thread
from tkinter import Tk, Button, Label, Text, Entry, END, Checkbutton, IntVar, StringVar, OptionMenu


# 利用TK组件创建一个图形界面类，加强用户反馈
class Applicaltion(object):
    def __init__(self):
        # 将WinIcacls类引入
        # self.acl = WinIcacls()

        # 下面开始创建图形框
        self.Windows = Tk()
        self.Windows.title('远or广共享文件小助手')
        # geometry 初始化窗口大小 中间'x'连接  初始位置 用‘+’连接
        self.Windows.geometry('1100x595+200+50')

        # pack 包 ，grid 网格，place 位置 三种排序定位
        # Label文本使用
        Label(self.Windows, text="1.输入路径名:").grid(row=0, column=1)
        Label(self.Windows, text="2.输入用户名:\n 多用户名如\n张三\n李四").grid(row=1, column=1)
        Label(self.Windows, text="3.输入服务器:").grid(row=2, column=1)

        # 输入框 Entry 用于显示简单的文本内容
        self.entry1 = Entry(self.Windows, width=140)
        self.entry1.grid(row=0, column=2, columnspan=6)
        # self.entry1.insert(0, r"C:\Users\csy\Desktop\runlike")

        self.entry2 = Text(self.Windows, width=60)
        self.entry2.grid(row=1, column=2, rowspan=1, columnspan=4)

        self.entry3 = Entry(self.Windows, width=60)
        self.entry3.grid(row=2, column=2, rowspan=1, columnspan=4)
        self.entry3.insert(0, "10.33.16.23")
        # self.entry3.insert(0, "ACER-CSY")

        # 权限选择多选框 只读R 只写W R执行 M修改 F全部
        self.chVar1 = IntVar()  # 用来获取复选框是否被勾选，通过chVarDis.get()来获取其的状态,其状态值为int类型 勾选为1  未勾选为0
        # text为该复选框后面显示的名称, variable将该复选框的状态赋值给一个变量，当state='disabled'时，该复选框为灰色，不能点的状态
        check1 = Checkbutton(self.Windows, text="只读复制", variable=self.chVar1)
        # 该复选框是否默认勾选,select为勾选, deselect为不勾选
        check1.select()
        check1.grid(row=3, column=2)
        # sticky=N：北/上对齐  S：南/下对齐  W：西/左对齐  E：东/右对齐

        self.chVar2 = IntVar()
        check2 = Checkbutton(self.Windows, text="读写参与", variable=self.chVar2)
        check2.deselect()
        check2.grid(row=3, column=3)

        self.chVar3 = IntVar()
        check3 = Checkbutton(self.Windows, text="完全控制F", variable=self.chVar3)
        check3.deselect()  # 默认不选
        check3.grid(row=3, column=4)

        self.chVar4 = IntVar()
        check4 = Checkbutton(self.Windows, text="递归继承", variable=self.chVar4)
        check4.deselect()  # 默认不选
        check4.grid(row=3, column=5)

        # 读取配置文件内容
        with open('config.txt', 'r', encoding='utf-8-sig') as f:
            self.OPTIONS = eval(f.read())
        # 读取添加常用路径选择框
        self.var = StringVar()
        self.var.set("速选")
        OptionMenu(self.Windows, self.var, *self.OPTIONS).grid(row=3, column=1)

        # 添加按钮框Button1
        self.submit_btn1 = Button(self.Windows, text='添加权限',
                                  command=lambda func='submit_grant': self.socket_client(func))
        # 如果点击输入的按钮是Return
        self.submit_btn1.bind_all("<Return>", self.key)
        # self.submit_btn.bind_all("<Key>",self.key)
        self.submit_btn1.grid(row=4, column=1)

        # 删除按钮框Button2
        self.submit_btn2 = Button(self.Windows, text='删除权限',
                                  command=lambda func='submit_remove': self.socket_client(func))
        self.submit_btn2.bind_all("<Return>", self.key)
        self.submit_btn2.grid(row=4, column=2)

        self.submit_btn3 = Button(self.Windows, text='查询授权',
                                  command=lambda func='query_grant': self.socket_client(func))
        # self.clean_btn.bind_all("<DELETE>",self.key)
        self.submit_btn3.grid(row=4, column=3)

        self.submit_btn4 = Button(self.Windows, text='清空输入', command=self.clean_entry)
        self.submit_btn4.grid(row=4, column=4)

        self.submit_btn5 = Button(self.Windows, text='备份权限',
                                  command=lambda func='backup_grant': self.socket_client(func))
        self.submit_btn5.grid(row=4, column=5)

        self.submit_btn6 = Button(self.Windows, text='慎点:强制获取管理员',
                                  command=lambda func='force_grant': self.socket_client(func))
        self.submit_btn6.grid(row=5, column=6)

        self.submit_btn7 = Button(self.Windows, text='查看文件夹',
                                  command=lambda func='ll_dir': self.socket_client(func))
        self.submit_btn7.grid(row=5, column=1)

        self.submit_btn8 = Button(self.Windows, text='新建文件夹',
                                  command=lambda func='mk_dir': self.socket_client(func))
        self.submit_btn8.grid(row=5, column=2)

        self.submit_btn9 = Button(self.Windows, text='删除文件夹',
                                  command=lambda func='rd_dir': self.socket_client(func))
        self.submit_btn9.grid(row=5, column=3)

        # 文本展示框 Text用于显示多行文本
        self.result_text = Text(self.Windows, height=40, background='#ccc')
        self.result_text.grid(row=1, column=6, rowspan=4, padx=5, pady=5)

    # 绑定键盘 bind_all('<Return>',函数)  == ENTER
    def key(self, event=None):
        # self.submit_grant()
        pass

    # 清空按钮文本框
    def clean_entry(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)

    # 将目录值，用户，权限，是否递归，发送
    def query_grant(self):
        # 1.从输入框获取用户值,需要向Text.get()函数传递一个开始和停止索引，以指示所需的Text小部件中文本的哪一部分'1.0'为全部获取。
        # 如果路径名为空则去速选栏搜索

        if self.entry1.get().strip() == "" and self.var.get() == "速选":
            print(str("必须输入或选择路径"))
            ls_dir = ''
        elif self.entry1.get().strip() == "":
            ls_dir = self.OPTIONS[self.var.get()]
            print(ls_dir)
        else:
            ls_dir = self.entry1.get().strip().rstrip('\\')

        if self.chVar3.get() == 1:
            perm = "(OI)(CI)(F)"  # 管理员完全控制
        elif self.chVar2.get() == 1:
            perm = "(OI)(CI)(M)"  # 读写参与
        elif self.chVar1.get() == 1:
            perm = "(OI)(CI)(RX)"  # 只读
        else:
            perm = ""

        if self.chVar4.get() == 1:
            rec = r"/T"  # 递归
        else:
            rec = ""

        users = self.entry2.get('1.0', END).strip().split()

        # iter迭代器配合next跳过循环
        it = iter(users)
        users_list = []
        a = 0
        for i in it:
            if "@" in i:
                users_list.append(i + " " + users[a + 2])
                next(it)
            else:
                users_list.append(i)
            a += 1
        data = r"{0};{1};{2};{3}".format(ls_dir, perm, rec, users_list)
        # data = r"{0};{1};{2};{3}".format(ls_dir, perm, rec, users)
        return data

    # 设置套接字
    def socket_client(self, func):
        # 创建 socket 对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置端口号
        port = 9999

        # 获取本地主机名
        # host = socket.gethostname()
        host = self.entry3.get().strip()

        try:
            s.connect((host, port))
            # 获取界面参数整合  C:\Users\csy\Desktop\runlike   ACER-CSY
            client_data = self.query_grant()
            send_data = "{0};{1}".format(func, client_data)

            # 发送
            s.sendall(send_data.encode('utf-8'))
            print('发送给服务端的数据>>>', send_data)
        except Exception as Error:
            # 3.将结果显示在下面的文本框Text控件
            self.result_text.delete(1.0, END)
            self.result_text.insert(END, str(Error))

        # 持续接收服务器发来大于 1024 字节的数据
        total_data = ""
        while True:
            server_data = s.recv(1024).decode('utf-8', 'ignore')
            total_data += server_data
            if not len(server_data):
                break

        print('接收到服务端的数据>>>', total_data)

        s.close()
        # 3.将结果显示在下面的文本框Text控件
        self.result_text.delete(1.0, END)
        self.result_text.insert(END, total_data)

    #  一直监听死循环
    def run(self):
        self.Windows.mainloop()


if __name__ == '__main__':
    app = Applicaltion()
    client_th = Thread(target=app.run())
    # 设置线程为守护线程，防止退出主线程时，子线程仍在运行
    client_th.setDaemon(True)
    # 新线程启动
    client_th.start()
