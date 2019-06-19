import json
import os


class UniversalModel(object):

    def center_window(self, root, width, height):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
        root.geometry(size)

    def readUser(self):
        info = {}
        try:
            with open('sec.json', 'rb') as file:
                info = json.load(file)
        except json.JSONDecodeError:
            pass
        except FileNotFoundError:
            with open('sec.json', 'wb') as file:
                pass
        if 'username' in info.keys():
            return self.md5To(info['username'])
        else:
            return ""

    def writeUser(self, user, pwd):
        info = {}
        try:
            with open('sec.json') as file:
                info = json.load(file, encoding='utf-8')
        except json.JSONDecodeError:
            pass
        with open('sec.json', 'w') as file:
            username = self.toMd5(user)
            info['username'] = username
            password = self.toMd5(pwd)
            info['password'] = password
            json.dump(info, file)

    def readPassword(self):
        info = {}
        try:
            with open('sec.json', 'rb') as file:
                info = json.load(file)
        except json.JSONDecodeError:
            pass
        if 'password' in info.keys():
            return self.md5To(info['password'])
        else:
            return ""

    def toMd5(self, string, salt="cfc830"):
        key = (48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65)
        string += salt
        string = bytearray(string.encode("gbk"))
        news = ""
        for i, str in enumerate(string):
            str -= i
            news += chr(str)
        return news

    def md5To(self, string, salt="cfc830"):
        string = bytearray(string.encode("gbk"))
        old = ""
        for i, str in enumerate(string):
            str += i
            old += chr(str)
        old = old.replace(salt, "")
        return old

    def read_file_path(self):
        info = {}
        try:
            with open('sec.json', 'rb') as file:
                info = json.load(file)
        except json.JSONDecodeError:
            pass
        if 'file_path' in info.keys():
            return info['file_path']
        else:
            return os.getcwd()+r"\no_match_ser.txt"

    def writeFilePath(self, path):
        info = {}
        try:
            with open('sec.json') as file:
                info = json.load(file, encoding='utf-8')
        except json.JSONDecodeError:
            pass
        with open('sec.json', 'w') as file:
            info['file_path'] = path
            json.dump(info, file)
