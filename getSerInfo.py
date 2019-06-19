from bs4 import BeautifulSoup
from re import findall, match


class getJFQTinfo(object):
    def __init__(self, html):
        self.soup = BeautifulSoup(html, features="html.parser")
        self.__keys = ('package_id', 'package_name', 'detail_name', 'detailtotal', 'detailremain', 'eff_date', 'exp_date')

    def getBundleinfo(self):
        # soup = BeautifulSoup(open('bs4.html', 'rb'), features="html.parser")
        # packageFlows = getTableText(soup.find_all(id='packageFlowsbodyID'))
        datagrid = self.__getTableText(self.soup.find_all(name='table', attrs='datagrid-btable'))
        # dljs = getTableText(soup.find_all(id='procDljsState'))
        if datagrid:
            return self.__dictDataGrid(datagrid[0])
        else:
            return datagrid

    def getUseInfoCqd(self):
        # soup = BeautifulSoup(open('bs41.html', 'rb'), features="html.parser")
        Msgs = self.__getTableText(self.soup.find_all(id='freeMsgPanel'))
        if Msgs:
            freemsg = []
            for msg in Msgs[0]:
                if msg:
                    freemsg.append(msg)
                else:
                    pass
            return self.__dictUseinfo(freemsg)
        else:
            return Msgs

    def __getTableText(self, tablesoup):
        return [[[td.get_text().strip() for td in tr.find_all('td')] for tr in data.find_all('tr')] for data in tablesoup]

    def __dictDataGrid(self, data):
        if data:
            dictlist = []
            for row in data:
                datadict = {}
                for index, value in enumerate(row):
                    if index in (1, 2):
                        if value.find("(") > -1 or value.find(")") > -1:
                            value = value.replace("(", "（").replace(")", "）")
                        datadict[self.__keys[index]] = value
                    elif index in (3, 4):
                        datadict[self.__keys[index]] = match("\d+(\.\d+)?", value).group()
                    elif index == 10:
                        datadict[self.__keys[5]] = value.replace("-", "")
                    elif index == 11:
                        datadict[self.__keys[6]] = value.replace("-", "")
                dictlist.append(datadict)
            return dictlist
        else:
            return data

    def __dictUseinfo(self, data):
        if data:
            dictlist = []
            datadict = {}
            for index, row in enumerate(data):
                # print(index,row)
                if index == 0:
                    pass
                else:
                    if index % 8 in (1, 2, 3, 4, 5):
                        datadict[self.__keys[index % 8 - 1]] = row[1]
                    elif index % 8 == 6:
                        datadict["business_type"] = row[1]
                    elif index % 8 == 7:
                        datadict[self.__keys[5]] = row[1]
                    elif index % 8 == 0:
                        datadict[self.__keys[6]] = row[1]
                        dictlist.append(datadict)
                        datadict = {}
            return self.__fluSwitch(dictlist)
        else:
            return data

    def __fluSwitch(self, dictlist):
        for data in dictlist:
            if data['business_type'].find('KB') > -1:
                data['detailtotal'] = self.__getTwoDecimalPlaces(int(findall('\d+', data['detailtotal'].split('(')[0])[0]))
                data['detailremain'] = self.__getTwoDecimalPlaces(int(findall('\d+', data['detailremain'].split('(')[0])[0]))
            else:
                data['detailtotal'] = int(findall('\d+', data['detailtotal'].split('(')[0])[0])
                data['detailremain'] = int(findall('\d+', data['detailremain'].split('(')[0])[0])
            data.pop('business_type')
        return dictlist

    def __getTwoDecimalPlaces(self, value):
        """
        四舍五不入获得两位小数
        :param value:
        :return:
        """
        if value >= 1048576:
            value = round(float(value) / 1024 / 1024, 10)
        elif value >= 1024:
            value = round(float(value) / 1024, 10)
        else:
            value = round(float(value)/10, 10)
        integer, decimal = str(value).split(".")
        length = len(decimal)
        if length == 1 or length == 2:
            return value
        else:
            return float(integer + "." + decimal[0] + decimal[1])


