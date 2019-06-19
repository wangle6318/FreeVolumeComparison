import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import filedialog
import json
from re import findall
from universal import UniversalModel
import threading
import traceback

from selenium import webdriver
from selenium.webdriver.ie.options import Options
from loginctc2 import LoginCtc, QueryJFQT
from getSerInfo import getJFQTinfo
from compare import Compare
from getAbpDatabase import getServiceNbrIter, getPackageDetail
# 创建主窗口


class LoginPage(object):

    def __init__(self, master=None):
        self.root = master
        self.__var_usr_name = tk.StringVar()
        self.__var_usr_pwd = tk.StringVar()
        self.__file_path = tk.StringVar()
        self.__um = UniversalModel()
        self.__pre = tk.IntVar()
        self.__pre0 = tk.IntVar()
        self.__pre1 = tk.IntVar()
        self.__pre2 = tk.IntVar()

        self.__prdY = tk.IntVar()
        self.__serY = tk.IntVar()

        self.__comObj0 = tk.IntVar()
        self.__comObj1 = tk.IntVar()
        self.__comObj2 = tk.IntVar()
        # 读取默认账号
        self.__var_usr_name.set(self.__um.readUser())
        self.__file_path.set(self.__um.read_file_path())

        self.login()

    def login(self):
        # 设置窗口大小,窗口居中
        self.__um.center_window(self.root, 400, 400)
        self.__loginpage = tk.Frame(self.root)
        self.__loginpage.pack()
        # 进入消息循环
        tk.Label(self.__loginpage, text="设置OA登陆账号", font=("宋体", 20)).grid(row=0, pady=40, columnspan=2)
        tk.Label(self.__loginpage, text="账号：", font=("宋体", 16)).grid(row=1, column=0, pady=10)
        tk.Label(self.__loginpage, text="密码：", font=("宋体", 16)).grid(row=2, column=0, pady=20)
        entry_usr_name = tk.Entry(self.__loginpage, textvariable=self.__var_usr_name, font=("宋体", 18), width=16)
        entry_usr_name.grid(row=1, column=1, pady=10)
        # 设置输入密码后显示*号
        entry_usr_pwd = tk.Entry(self.__loginpage, textvariable=self.__var_usr_pwd, font=("宋体", 18), width=16, show='*')
        entry_usr_pwd.grid(row=2, column=1, pady=20)
        enter_sure = tk.Button(self.__loginpage, command=self.__checklogin, text="确认设置", font=("宋体", 18), bg="#3072af", fg="white", relief="flat")
        enter_sure.grid(row=3, columnspan=2, pady=20)

        self.__loginpage.mainloop()

    def __checklogin(self):
        if self.__var_usr_name.get() and self.__var_usr_pwd.get():
            self.__um.writeUser(self.__var_usr_name.get(), self.__var_usr_pwd.get())
            self.__loginpage.destroy()
            self.main()
        else:
            showinfo(title='警告', message='账号或密码为空！')

    def main(self):
        self.__um.center_window(self.root, 800, 600)
        self.root.resizable(width=False, height=True)

        mainpage = tk.Frame(self.root)
        mainpage.pack()

        top = tk.Frame(mainpage)
        top.pack(side=tk.TOP)
        tk.Label(top, text="用户名："+self.__var_usr_name.get(), anchor="w", width=800).pack(side="top", padx=10)
        cv = tk.Canvas(top, width=800, height=5)
        cv.pack(side="bottom")
        cv.create_line(0, 5, 800, 5, fill="gray")

        middle1 = tk.Frame(mainpage)
        middle1.pack(side=tk.TOP, fill=tk.BOTH, padx=10)
        tk.Label(middle1, text="选择文件保存的位置:", anchor="w").grid(row=0, column=0)
        tk.Entry(middle1, textvariable=self.__file_path, width=50,  state="disabled").grid(row=0, column=1)
        tk.Button(middle1, text="打开", command=self.__setFilePath, relief="groove").grid(row=0, column=2, ipadx=20, padx=15)

        middle2 = tk.Frame(mainpage)
        middle2.pack(side=tk.TOP, fill=tk.BOTH, padx=10)
        self.__setPrePay(middle2)

        middle3 = tk.Frame(mainpage)
        middle3.pack(side=tk.TOP, fill=tk.BOTH, padx=10)

        middle31 = tk.Frame(middle3, bd="2", bg="#F0F0F0", relief="groove")
        middle31.pack(side=tk.LEFT, anchor=tk.N)
        self.__setUserStatus(middle31)

        middle32 = tk.Frame(middle3, bd="2", bg="#F0F0F0", relief="groove")
        middle32.pack(side=tk.LEFT, anchor=tk.N, padx=10, ipady=6,ipadx=20)
        self.__inputPrdId(middle32)

        bottom = tk.Frame(mainpage)
        bottom.pack(side=tk.TOP, fill=tk.BOTH)

        bottom1 = tk.Frame(bottom, bd="2", bg="#F0F0F0", relief="groove")
        bottom1.pack(side=tk.LEFT, anchor=tk.N, padx=10, pady=10, ipadx=11)
        self.__inputSerNbr(bottom1)

        bottom2 = tk.Frame(bottom)
        bottom2.pack(side=tk.LEFT, pady=10)
        self.__setComObj(bottom2, mainpage)

        mainpage.mainloop()

    def __saveConfig(self, start):
        config = {}
        try:
            with open('sec.json') as file:
                config = json.load(file, encoding='utf-8')
        except json.JSONDecodeError:
            pass
        with open('sec.json', 'w') as file:
            config['file_path'] = self.__file_path.get()
            if self.__pre.get():
                config['attribute'] = ["-1"]
            else:
                attr = []
                if self.__pre0.get():
                    attr.append("0")
                if self.__pre1.get():
                    attr.append("1")
                if self.__pre2.get():
                    attr.append("2")
                config['attribute'] = attr
            config['ifstate'] = findall("\d{4}", self.__box.get())
            config['iflimitproc'] = self.__prdY.get()
            config['proc_id'] = findall("[a-zA-Z0-9-]+", self.__prdList.get())
            config['ifinputser'] = self.__serY.get()
            config['service_nbr'] = findall("[a-zA-Z0-9-]+", self.__serList.get())
            if self.__comObj0.get() == 1:
                config['compare_obj'] = '12'
            elif self.__comObj1.get() == 1:
                config['compare_obj'] = '1'
            elif self.__comObj2.get() == 1:
                config['compare_obj'] = '2'
            json.dump(config, file)
            if config['ifstate']:
                start['state'] = 'normal'
            else:
                showinfo(title="警告", message="用户状态不能为空")
                return
            if config['iflimitproc']:
                if not config['proc_id']:
                    start['state'] = 'disabled'
                    showinfo(title="警告", message="限定产品时产品ID不能为空")
                    return
            if config['ifinputser']:
                if not config['service_nbr']:
                    start['state'] = 'disabled'
                    showinfo(title="警告", message="限定设备时设备号不能为空")

    def __setComObj(self, root, mainpage):
        bottom21 = tk.Frame(root, bd="2", bg="#F0F0F0", relief="groove")
        bottom21.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        tk.Label(bottom21, text="数据库比较对象选择:", anchor="w").grid(row=0, column=0)
        all = tk.Checkbutton(bottom21, text="全部", variable=self.__comObj0, command=lambda: self.__checkComObjValue())
        all.grid(row=0, column=1)
        bundle = tk.Checkbutton(bottom21, text="套餐使用情况数据", variable=self.__comObj1, command=lambda: self.__checkComObjValue(False))
        bundle.select()
        bundle.grid(row=0, column=2)
        cqd = tk.Checkbutton(bottom21, text="CQD数据", variable=self.__comObj2, command=lambda: self.__checkComObjValue(False))
        cqd.grid(row=0, column=3)

        bottom22 = tk.Frame(root)
        bottom22.pack(side=tk.TOP, pady=60)

        savebtn = tk.Button(bottom22, text="保存设置", font=(14,), width=45, bg="#4C8EE0", fg="white",
                            command=lambda: self.__saveConfig(startbtn))
        savebtn.grid(ipady=5, row=1, sticky=tk.S)
        startbtn = tk.Button(bottom22, text="启动程序", font=(14,), width=45, bg="#4C8EE0", fg="white", state="disabled",
                             command=lambda: self.__checkStart(mainpage))
        startbtn.grid(ipady=5, row=2, sticky=tk.N)

    def __checkComObjValue(self, status=True):
        if status:
            if self.__comObj0.get() == 1:
                self.__comObj1.set(0)
                self.__comObj2.set(0)
        else:
            if self.__comObj0.get() == 1:
                self.__comObj0.set(0)
            elif self.__comObj1.get() == 1 and self.__comObj2.get() == 1:
                self.__comObj0.set(1)
                self.__comObj1.set(0)
                self.__comObj2.set(0)
            if self.__comObj1.get() == 0 and self.__comObj2.get() == 0:
                self.__comObj0.set(1)

    def __inputSerNbr(self, root):
        tk.Label(root, text="是否输入设备:").grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(root, variable=self.__serY, value=1, text="是", command=lambda: self.__limitEntryState(self.__serY.get(), ser, box)).grid(row=0, column=1)
        tk.Radiobutton(root, variable=self.__serY, value=0, text="否", command=lambda: self.__limitEntryState(self.__serY.get(), ser, box)).grid(row=0, column=2, sticky=tk.W)

        ser_text = tk.StringVar()
        tk.Label(root, text="输入设备号:").grid(row=1, column=0, sticky=tk.W)
        ser = tk.Entry(root, width=20, textvariable=ser_text)
        ser['state'] = "disabled"
        ser.grid(row=1, column=1, columnspan=2, sticky=tk.W)
        tk.Button(root, text="确定输入", relief="groove", command=lambda: self.__inputSerToBox(ser_text, box)).grid(row=1, column=3, sticky=tk.W, padx=20)
        tk.Button(root, text="清空", relief="groove", command=lambda: ser_text.set("")).grid(row=1, column=4, sticky=tk.W)

        self.__serList = tk.StringVar()
        box = tk.Listbox(root, listvariable=self.__serList, selectmode="extended", highlightcolor="#f0f0f0")
        box['state'] = "disabled"
        box.grid(row=2, rowspan=3, column=0, columnspan=4, ipadx=120, ipady=55, sticky=tk.W)
        tk.Scrollbar(box, command=box.yview).pack(side=tk.RIGHT, fill=tk.Y)
        clear = tk.Button(root, text="清空", relief="groove", command=lambda: box.delete(0, tk.END))
        clear.grid(row=2, column=3, columnspan=2, pady=10, ipadx=12, sticky=tk.SE)
        delete = tk.Button(root, text="删除", relief="groove",
                           command=lambda: [box.delete(i - index) for index, i in enumerate(box.curselection())])
        delete.grid(row=3, column=3, columnspan=2, pady=10, ipadx=12, sticky=tk.E)

    def __limitEntryState(self, value, ent, box):
        if value:
            ent['state'] = 'normal'
            box['state'] = 'normal'
            box['cursor'] = 'hand2'
        else:
            ent['state'] = 'disabled'
            box['state'] = 'disabled'
            box['cursor'] = 'arrow'

    def __inputPrdId(self, root):
        tk.Label(root, text="是否限定产品:").grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(root, variable=self.__prdY, value=1, text="是", command=lambda:self.__limitEntryState(self.__prdY.get(), prd, box)).grid(row=0, column=1)
        tk.Radiobutton(root, variable=self.__prdY, value=0, text="否", command=lambda:self.__limitEntryState(self.__prdY.get(), prd, box)).grid(row=0, column=2, sticky=tk.W)

        ser_text = tk.StringVar()
        tk.Label(root, text="输入产品编码:").grid(row=1, column=0, sticky=tk.W)
        prd = tk.Entry(root, width=20, textvariable=ser_text)
        prd['state'] = "disabled"
        prd.grid(row=1, column=1, columnspan=2, sticky=tk.W)
        tk.Button(root, text="确定输入", relief="groove", command=lambda: self.__inputSerToBox(ser_text, box)).grid( \
            row=1, column=3, sticky=tk.W, padx=20)
        tk.Button(root, text="清空", relief="groove", command=lambda: ser_text.set("")).grid(row=1, column=4, sticky=tk.W)

        self.__prdList = tk.StringVar()
        box = tk.Listbox(root, listvariable=self.__prdList, selectmode="extended", highlightcolor="#f0f0f0")
        box['state'] = "disabled"
        box.grid(row=2, rowspan=3, column=0, columnspan=4, ipadx=120, ipady=55, sticky=tk.W)
        tk.Scrollbar(box, command=box.yview).pack(side=tk.RIGHT, fill=tk.Y)
        clear = tk.Button(root, text="清空", relief="groove", command=lambda: box.delete(0, tk.END))
        clear.grid(row=2, column=3, columnspan=2, pady=10, ipadx=12, sticky=tk.SE)
        delete = tk.Button(root, text="删除", relief="groove",\
                           command=lambda: [box.delete(i - index) for index, i in enumerate(box.curselection())])
        delete.grid(row=3, column=3, columnspan=2, pady=10, ipadx=12, sticky=tk.E)

    def __inputSerToBox(self, ser_text, box):
        ser_list = []
        text = ser_text.get()
        ser_text.set("")
        if text != "":
            temp_list1 = text.split(",")
            temp_list2 = []
            temp_list3 = []
            for ser in temp_list1:
                temp_list2 += ser.split("，")
            for ser in temp_list2:
                temp_list3 += ser.split(" ")
            for ser in temp_list3:
                ser_list += ser.split("\n")
        for ser in ser_list:
            if ser != "" and ser not in box.get(0, tk.END):
                box.insert(tk.END, findall("[a-zA-Z0-9-]+", ser))

    def __setUserStatus(self, root):
        tk.Label(root, text="设置用户状态:").grid(row=0, column=0, sticky=tk.W)
        options = ['1001，正常', '1002，改号', '1003，已归档', '1101，拆机', '1102，欠费拆机', '1103，预拆机/冷冻停机',
                   '1104，锁定状态', '1105，删除', '1107，预销户', '1109，实时拆机', '1201，申请停机', '1202，双停',
                   '1203，单停+申请停机', '1204，双停+申请停机', '1205，单停', '1206，申请停机+预拆机',
                   '1209，历史申请停机', '1301，催缴', '1401，注销', '2001，挂失状态', '2002，违章停机',
                   '2003，涉案违章停机', '2004，实名不合规单向停机', '2005，实名不合规双向停机', '2006，12321举报违章停机',
                   '2007，10000举报违章停机', '2009，一证五卡不合规单停', '2010，一证五卡不合规双停', '3001，预实例状态',
                   '3002，预开通', '4001，拆线保号', '5001，紧急复机', '5002，高额停机', '5003，高额复机']

        self.__ust = tk.StringVar()
        self.__ust.set(options[0])
        ust = ttk.Combobox(root, textvariable=self.__ust, values=options, state='readonly', width=25)
        ust.grid(row=0, column=1, columnspan=3, sticky=tk.W)

        tk.Button(root, text="确定选择", relief="groove", command=lambda: self.__boxToListBox(box)).grid(row=0, column=4, sticky=tk.E)

        self.__box = tk.StringVar()
        box = tk.Listbox(root, listvariable=self.__box, selectmode="extended", highlightcolor="#f0f0f0", cursor="hand2")
        box.grid(row=1, column=0, columnspan=5, ipadx=180, ipady=50)
        box.insert(tk.END, self.__ust.get())
        tk.Scrollbar(box, command=box.yview).pack(side=tk.RIGHT, fill=tk.Y)

        clear = tk.Button(root, text="清空", relief="groove", command=lambda: box.delete(0, tk.END))
        clear.grid(row=2, column=0, pady=10)

        delete = tk.Button(root, text="删除", relief="groove", command=lambda: [box.delete(i-index) for index, i in enumerate(box.curselection())])
        delete.grid(row=2, column=4, pady=10, sticky=tk.W)

    def __boxToListBox(self, object):
        if self.__ust.get() in self.__box.get():
            showinfo(title='警告', message="["+self.__ust.get()+"] 已选择，不可重复选择")
        else:
            object.insert(tk.END, self.__ust.get())

    def __setPrePay(self, root):
        tk.Label(root, text="设置预后属性:").grid(row=0, column=0, sticky=tk.W)
        pre = tk.Checkbutton(root, text="全部", variable=self.__pre, command=lambda: self.__checkPrePayValue())
        pre.select()
        pre.grid(row=0, column=1, sticky=tk.W)
        pre0 = tk.Checkbutton(root, text="预付费", variable=self.__pre0, command=lambda: self.__checkPrePayValue(False))
        pre0.grid(row=0, column=2, sticky=tk.W)
        pre1 = tk.Checkbutton(root, text="后付费", variable=self.__pre1, command=lambda: self.__checkPrePayValue(False))
        pre1.grid(row=0, column=3, sticky=tk.W)
        pre2 = tk.Checkbutton(root, text="准预付费", variable=self.__pre2,
                              command=lambda: self.__checkPrePayValue(False))
        pre2.grid(row=0, column=4, sticky=tk.W)

    def __checkPrePayValue(self, status=True):
        if status is True:
            if self.__pre.get() == 1:
                self.__pre0.set(0)
                self.__pre1.set(0)
                self.__pre2.set(0)
        else:
            if self.__pre.get() == 1:
                self.__pre.set(0)
            elif self.__pre0.get() == 1 and self.__pre1.get() == 1 and self.__pre2.get() == 1:
                self.__pre.set(1)
                self.__pre0.set(0)
                self.__pre1.set(0)
                self.__pre2.set(0)
            if self.__pre0.get() == 0 and self.__pre1.get() == 0 and self.__pre2.get() == 0:
                self.__pre.set(1)

    def __setFilePath(self):
        file = filedialog.asksaveasfilename(initialdir="/")
        if file:
            self.__file_path.set(file)
            self.__um.writeFilePath(file)

    def __checkStart(self, mainpage):
        mainpage.destroy()
        self.__startApp()

    def __sureStart(self, box1, box2):
        try:
            thread = threading.Thread(target=lambda: self.__start(box1, box2))
            thread.start()
        except Exception as e:
            traceback.print_exc(file=open('error.log', 'w+', encoding='utf-8'))

    def __startApp(self):
        self.__um.center_window(self.root, 800, 600)
        self.root.resizable(width=False, height=False)

        comparepage = tk.Frame(self.root)
        comparepage.pack()

        top = tk.Frame(comparepage)
        top.pack(side=tk.TOP)
        tk.Label(top, text="用户名：" + self.__var_usr_name.get(), anchor="w", width=800).pack(side="top", padx=10)
        tk.Button(top, text="确认启动", command=lambda: self.__sureStart(box1, box2)).pack()
        cv = tk.Canvas(top, width=800, height=5)
        cv.pack(side="bottom")
        cv.create_line(0, 5, 800, 5, fill="gray")

        middle = tk.Frame(comparepage)
        middle.pack(side=tk.TOP, fill=tk.BOTH, padx=10)

        middleleft = tk.Frame(middle, bd="2", bg="#F0F0F0", relief="groove")
        middleleft.pack(side=tk.LEFT, anchor=tk.N, padx=5)

        self.__allser = tk.StringVar()
        tk.Label(middleleft, text="已查询的设备列表").grid(row=0, sticky=tk.W)
        box1 = tk.Listbox(middleleft, listvariable=self.__allser, selectmode="extended", highlightcolor="#f0f0f0")
        box1.grid(row=1, rowspan=3, column=0, columnspan=4, ipadx=175, ipady=100, sticky=tk.W)
        tk.Scrollbar(box1, command=box1.yview).pack(side=tk.RIGHT, fill=tk.Y)

        middleright = tk.Frame(middle, bd="2", bg="#F0F0F0", relief="groove")
        middleright.pack(side=tk.LEFT, anchor=tk.N, padx=10)

        self.__difser = tk.StringVar()
        tk.Label(middleright, text="免费量不一致的设备列表").grid(row=0, sticky=tk.W)
        box2 = tk.Listbox(middleright, listvariable=self.__difser, selectmode="extended", highlightcolor="#f0f0f0")
        box2.grid(row=1, rowspan=3, column=0, columnspan=4, ipadx=175, ipady=100, sticky=tk.W)
        tk.Scrollbar(box2, command=box2.yview).pack(side=tk.RIGHT, fill=tk.Y)

        comparepage.mainloop()
        # self.__start(box1, box2)

    def __start(self, box1, box2):
        driver = webdriver.Ie()
        LoginCtc(driver)
        search = QueryJFQT(driver)
        pack = getPackageDetail()

        for service_nbr in getServiceNbrIter():
            bundle, useinfo = search.queryValue(service_nbr)
            webdata = []
            cqddata = []
            if bundle:
                webdata = getJFQTinfo(bundle).getBundleinfo()
            if useinfo:
                cqddata = getJFQTinfo(useinfo).getUseInfoCqd()
            oracledata = pack.getFreeVolume(service_nbr)
            compare = Compare(service_nbr)
            dif_ser = None
            if bundle:
                dif_ser = compare.bundleDataCompare(webdata, oracledata)
            if useinfo:
                dif_ser = compare.cqdDataCompare(cqddata, oracledata)
            box1.insert(tk.END, service_nbr)
            if dif_ser is not None:
                box2.insert(tk.END, dif_ser)

if __name__ == '__main__':
    try:
        window = tk.Tk()
        window.title('免费量信息比对程序')
        LoginPage(window)
        window.mainloop()
    except Exception as e:
        traceback.print_exc(file=open('error.log', 'w+', encoding='utf-8'))
