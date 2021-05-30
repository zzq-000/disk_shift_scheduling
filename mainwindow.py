import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import login


def getDis(a: list) -> int:
    return a[1]


class mainwindow():

    def reback(self):
        self.initface.destroy()
        login.login(self.root)

    def print(self):
        x = self.tree.get_children()
        for i in x:
            self.tree.delete(i)
        seq = ''
        move = ''
        res = 0
        for i in self.result:
            seq += str(i) + " "
        for i in range(len(self.move)):
            res += self.move[i]
            if i == 0:
                move += str(self.move[i])
            else:
                move += "+" + str(self.move[i])
            if i == len(self.move) - 1:
                move += "=" + str(res)
        self.tree.insert("", 0, values=(seq, move))
        self.tree.pack(side=BOTTOM)
        return

    def prepro(self):
        if self.e1.get() != '':
            self.total = int(self.e1.get())
        if self.e2.get() != '':
            self.pos = int(self.e2.get())
        if self.e3.get() is None:
            tkinter.messagebox.showinfo("警告", '请输入磁盘请求序列')
        else:
            s = str(self.e3.get())
            temp = ''
            for i in range(len(s)):
                if s[i] == ' ':
                    if int(temp)>self.total:
                        tkinter.messagebox.showinfo("警告","请求不合法")
                        return
                    self.call.append(int(temp))
                    temp = ''
                else:
                    temp += s[i]
            if int(temp) > self.total:
                tkinter.messagebox.showinfo("警告", "请求不合法")
                return
            self.call.append(int(temp))
        return

    def SSTF(self):
        self.prepro()
        tool = []
        for i in self.call:
            a = []
            a.append(i)
            a.append(abs(i - self.pos))
            tool.append(a)
        tool.sort(key=getDis)
        while len(tool) != 0:
            t = tool.pop(0)
            self.result.append(t[0])
            self.pos = t[0]
            self.move.append(t[1])
            for i in tool:
                i[1] = abs(i[0] - self.pos)
            tool.sort(key=getDis, reverse=False)
        self.print()
        self.result.clear()
        self.call.clear()
        self.move.clear()
        self.pos=self.atom
        return

    def SCAN(self):
        self.prepro()
        tool = [0] * (self.total + 1)
        left = self.total + 1
        right = - 1
        length = self.total + 1
        min = 0
        for i in self.call:
            tool[i] = 1
            if i < left:
                left = i
            if i > right:
                right = i
            if abs(i - self.pos) < min:
                length = abs(i - self.pos)
                min = i
        foot = self.pos
#        if min >= self.pos:
        while foot <= right:
            if tool[foot] == 1:
                tool[foot] = 0
                self.result.append(foot)
                self.move.append(foot - self.pos)
                self.pos = foot
            foot += 1
        while foot >= left:
            if tool[foot] == 1:
                tool[foot] = 0
                self.result.append(foot)
                self.move.append(self.pos - foot)
                self.pos = foot
            foot -= 1
        # else:
        #     while foot >= left:
        #         if tool[foot] == 1:
        #             tool[foot] = 0
        #             self.result.append(foot)
        #             self.move.append(self.pos - foot)
        #             self.pos = foot
        #         foot -= 1
        #     while foot <= right:
        #         if tool[foot] == 1:
        #             tool[foot] = 0
        #             self.result.append(foot)
        #             self.move.append(foot - self.pos)
        #             self.pos = foot
        #         foot += 1
        self.print()
        self.result.clear()
        self.call.clear()
        self.move.clear()
        self.pos=self.atom
        return

    def __init__(self, master):
        self.root = master
        self.root.title('管理')
        self.initface = Frame(self.root, )
        self.initface.pack()
        self.total = 200
        self.pos = 100
        self.atom=self.pos
        self.call = []
        self.move = []
        self.result = []
        lb2 = Label(self.initface, text='磁头总数')
        lb2.grid(row=1, column=1, padx=5)
        lb3 = Label(self.initface, text='磁头初始位置')
        lb3.grid(row=1, column=2, padx=5)
        lb4 = Label(self.initface, text='磁盘请求序列')
        lb4.grid(row=1, column=3, padx=5)


        lb1 = Label(self.initface, text='请输入初始条件：')
        lb1.grid(row=2, column=0)
        self.e1 = Entry(self.initface, width=5)
        self.e1.grid(row=2, column=1)
        self.e2 = Entry(self.initface, width=5)
        self.e2.grid(row=2, column=2)
        self.e3 = Entry(self.initface, width=40)
        self.e3.grid(row=2, column=3)


        btnsure1 = Button(self.initface, text='SSTF', fg='black', font=('黑体', 9), command=self.SSTF)
        btnsure1.grid(row=4, column=0, padx=10, pady=10)
        btnsure2 = Button(self.initface, text='SCAN', fg='black', font=('黑体', 9), command=self.SCAN)
        btnsure2.grid(row=4, column=1, padx=10, pady=10)
        btnsure3 = Button(self.initface, text='退出登录', fg='black', font=('黑体', 9), command=self.reback)
        btnsure3.grid(row=4, column=2, padx=10, pady=10)


        columns = (("响应请求顺序", "移臂总量"))
        self.tree = ttk.Treeview(self.root, height=22, show="headings", columns=columns)  # #创建表格对象
        self.tree.column("响应请求顺序", width=200)  # #设置列
        self.tree.column("移臂总量", width=240)
        self.tree.heading("响应请求顺序", text="响应请求顺序")  # #设置显示的表头名
        self.tree.heading("移臂总量", text="移臂总量")
