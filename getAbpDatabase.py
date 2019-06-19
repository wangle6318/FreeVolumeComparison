import cx_Oracle
import datetime
import json


class getServiceNbrIter(object):
    """
    从数据库获得设备号，并且放入迭代器中
    """
    def __init__(self, max=1000000):
        self.__n = 0
        self.__max = max
        self.__db = cx_Oracle.connect('xxxxxxxx', 'xxx', 'xx.x.xx.xxxx:xxxx/xxxxx')
        sql = self.__sqlString()
        self.__cursor = self.__db.cursor()
        self.__cursor.execute(sql)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__n < self.__max:
            try:
                data = self.__cursor.fetchone()[0]
            except TypeError:
                raise StopIteration
            self.__n += 1
            return data
        self.__cursor.close()
        self.__db.close()
        raise StopIteration

    def __sqlString(self):
        config = {}
        try:
            with open('sec.json', 'rb') as file:
                config = json.load(file)
        except json.JSONDecodeError:
            pass
        sql_head = "SELECT service_nbr FROM hss.tb_xxxx_xxxx_xx"
        sql_condition1 = ""
        if config['attribute'] == ["-1"]:
            sql_condition1 = " "
        else:
            sql_condition1 = self.__addCondition('if_prepay', config['attribute'])
        sql_condition2 = self.__addCondition('prd_inst_stas_id', config['ifstate'])
        sql_condition3 = self.__addCondition('prd_id', config['proc_id'], flag=config['iflimitproc'])
        sql_condition4 = self.__addCondition('service_nbr', config['service_nbr'], flag=config['ifinputser'])
        sql = sql_head + " where " + sql_condition2
        if config['attribute'] != ["-1"]:
            sql += " and " + sql_condition1
        if config['iflimitproc']:
            sql += " and " + sql_condition3
        if config['ifinputser']:
            sql += " and " + sql_condition4
        return sql

    def __addCondition(self, condition, content, flag=1):
        if flag:
            condition += " in ("
            length = len(content)
            for index, attribute in enumerate(content):
                condition += "\'" + attribute + "\'"
                if index != length - 1:
                    condition += ","
            condition += ")"
            return condition
        else:
            return " "

class getPackageDetail(object):
    """
    从数据库获得免费量数据
    """
    def __init__(self):
        self.__keys = ('package_id', 'package_name', 'detail_name', 'detailtotal', 'detailremain', 'eff_date', 'exp_date')
        self.__db = cx_Oracle.connect('xxxxxxxx', 'xxx', 'xx.x.xx.xxxx:xxxx/xxxxx')
        self.__cursor = self.__db.cursor()
        self.__billing_cycle = int(datetime.datetime.now().strftime("%Y%m"))

    def getFreeVolume(self, service_nbr):
        """
        获得免费量数据
        :param service_nbr:
        :return:
        """
        sql = "select t.packageid,a.ofr_name,t.DETAILNAME,t.DETAILTOTAL,t.DETAILREMAIN,t.EFF_DATE,t.EXP_DATE \
              from hss.c_xxxxxxxxxxxxxxx_xxxx t, hss.tb_xxxxxxxx_xxxxx a \
              where t.acctnum = :service_nbr and billing_cycle = :billing_cycle \
              and a.ofr_code = t.packageid order by t.billing_cycle"
        self.__cursor.execute(sql, {"service_nbr": service_nbr, "billing_cycle": self.__billing_cycle})
        data = self.__cursor.fetchall()
        return self.__dictFreevolumeInfo(data)

    def __dictFreevolumeInfo(self, data):
        """
        将免费量数据，字典化，并保存在列表中
        :param data:
        :return:列表
        """
        if data:
            dictlist = []
            for row in data:
                datadict = {}
                for index, value in enumerate(row):
                    if isinstance(value, datetime.datetime):
                        value = value.strftime("%Y%m%d")
                    elif isinstance(value, int) and row[2].find('通话') < 0 and row[2].find('短信') < 0 and row[2].find('小时') < 0:
                        value = self.__getTwoDecimalPlace(value)
                    # if isinstance(value, str) and value.find('（') >= 0:
                    #     value = value.replace('（', '(').replace('）', ')')
                    # elif isinstance(value, str) and value.find('（') >= 0:
                    #     value = value.replace('(', '（').replace(')', '）')
                    datadict[self.__keys[index]] = str(value)
                dictlist.append(datadict)
            return dictlist
        else:
            return data

    def __getTwoDecimalPlaces(self, value):
        """
        四舍五入获得两位小数
        :param value:
        :return:两位小数的浮点数
        """
        if value >= 1048576:
            value = round(float(value) / 1024 /1024, 10)
        elif value >= 1024:
            value = round(float(value) / 1024, 10)
        integer, decimal = str(value).split(".")
        length = len(decimal)
        if length == 1 or length == 2:
            return value
        elif int(decimal[2]) > 4:
            return round(float(integer+"."+decimal[0]+decimal[1]) + 0.01, 2)
        else:
            return float(integer+"."+decimal[0]+decimal[1])

    def __getTwoDecimalPlace(self, value):
        """
        四舍五不入获得两位小数
        :param value:
        :return:
        """
        if value >= 1048576:
            value = round(float(value) / 1024 /1024, 10)
        elif value >= 1024:
            value = round(float(value) / 1024, 10)
        else:
            value = round(float(value), 10)
        integer, decimal = str(value).split(".")
        length = len(decimal)
        if length == 1 or length == 2:
            return value
        else:
            return float(integer+"."+decimal[0]+decimal[1])

    def close(self):
        self.__cursor.close()
        self.__db.close()


if __name__ == '__main__':

    pack = getPackageDetail()
    # for ser in getServiceNbrIter():
    #     print(ser, pack.getFreeVolume(ser))

    a = pack.getFreeVolume('1234567890')
    print(a)
    pack.close()