from bs4 import BeautifulSoup
from re import findall


class getJFQTinfo(object):
    def __init__(self):
        # self.soup = BeautifulSoup(html, features="html.parser")
        self.__keys = ('package_id', 'package_name', 'detail_name', 'detailtotal', 'detailremain', 'eff_date', 'exp_date')

    def getUseInfoComparison(self):
        soup = BeautifulSoup(open('bs1.html', 'rb'), features="html.parser")
        Msgs = self.__getTableText(soup.find_all(id='freeMsgPanel'))
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

    def __dictUseinfo(self, data):
        if data:
            dictlist = []
            datadict = {}
            for index, row in enumerate(data):
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
            return self.fluSwitch(dictlist)
        else:
            return data

    def fluSwitch(self, dictlist):
        for data in dictlist:
            if data['business_type'].find('KB') > -1:
                data['detailtotal'] = self.__getTwoDecimalPlaces(int(findall('\d+', data['detailtotal'].split('(')[0])[0]))
                data['detailremain'] = self.__getTwoDecimalPlaces(int(findall('\d+', data['detailremain'].split('(')[0])[0]))
                data.pop('business_type')
        return dictlist

    def __getTwoDecimalPlaces(self, value):
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

if __name__ == '__main__':
    g = getJFQTinfo()
    g.getUseInfoComparison()

    cqd = [{'package_id': '2-1QNLPDCG', 'package_name': '宽带网龄赠送0元800M+800M闲时国内流量包', 'detail_name': '国内上网（含黑莓上网，不含wifi）免800MB', 'detailtotal': 800.0, 'detailremain': 746.29, 'eff_date': '20190501000000', 'exp_date': '20190531235959'}, {'package_id': '2-1QNLPDCG', 'package_name': '宽带网龄赠送0元800M+800M闲时国内流量包', 'detail_name': '国内上网（含黑莓上网，不含wifi）免800MB（晚23点到早7点）', 'detailtotal': 800.0, 'detailremain': 76.0, 'eff_date': '20190501000000', 'exp_date': '20190531235959'}, {'package_id': '2-1RRYD2OY', 'package_name': '爱听4G定向流量（6G）可选包', 'detail_name': '爱听4G包内专用国内上网（含黑莓上网，不含wifi）免6GB', 'detailtotal': 6.0, 'detailremain': 0.0, 'eff_date': '20190501000000', 'exp_date': '20190531235959'}, {'package_id': '2-1W35KMMW', 'package_name': '0元40GB国内达量降速可选包', 'detail_name': '国内上网（含黑莓上网，不含wifi）免40GB（群组共享）', 'detailtotal': 40.0, 'detailremain': 2.59, 'eff_date': '20190501000000', 'exp_date': '20190531235959'}, {'package_id': '2-1Y1ZJUKC', 'package_name': '十全十美畅享199元套餐（乐享家）', 'detail_name': '乐享家全国上网免4GB(群组共享)(上月结转)', 'detailtotal': 4.0, 'detailremain': 67.0, 'eff_date': '20190501000000', 'exp_date': '20190531235959'}, {'package_id': '2-1Y1ZJUKC', 'package_name': '十全十美畅享199元套餐（乐享家）', 'detail_name': '乐享家全国上网免4GB（群组共享）', 'detailtotal': 4.0, 'detailremain': 0.0, 'eff_date': '20190501000000', 'exp_date': '20190531235959'}, {'package_id': '2-2UL6EMUD', 'package_name': '十全十美套餐0元10G全国流量月包（5个月）', 'detail_name': '国内上网（含黑莓上网，不含wifi）免10GB（群组共享）', 'detailtotal': 10.0, 'detailremain': 0.0, 'eff_date': '20190501000000', 'exp_date': '20190531235959'}, {'package_id': '2-XIKXDFW', 'package_name': '2014年员工套餐WIFI时长包', 'detail_name': '国内wifi上网免120小时', 'detailtotal': '7200', 'detailremain': '0分钟', 'business_type': '分钟', 'eff_date': '20190501000000', 'exp_date': '20190531235959'}]
    web = [{'package_id': '2-XIKXDFW', 'package_name': '2014年员工套餐WIFI时长包', 'detail_name': '国内wifi上网免120小时', 'detailtotal': '7200', 'detailremain': '0', 'eff_date': '20171001', 'exp_date': '20510101'}, {'package_id': '2-1QNLPDCG', 'package_name': '宽带网龄赠送0元800M+800M闲时国内流量包', 'detail_name': '国内上网（含黑莓上网，不含wifi）免800MB', 'detailtotal': '800.0', 'detailremain': '800.0', 'eff_date': '20170301', 'exp_date': '20501230'}, {'package_id': '2-1QNLPDCG', 'package_name': '宽带网龄赠送0元800M+800M闲时国内流量包', 'detail_name': '国内上网（含黑莓上网，不含wifi）免800MB（晚23点到早7点）', 'detailtotal': '800.0', 'detailremain': '76.0', 'eff_date': '20170301', 'exp_date': '20501230'}, {'package_id': '2-1W35KMMW', 'package_name': '0元40GB国内达量降速可选包', 'detail_name': '国内上网（含黑莓上网，不含wifi）免40GB（群组共享）', 'detailtotal': '40.0', 'detailremain': '2.59', 'eff_date': '20171001', 'exp_date': '20500102'}, {'package_id': '2-1Y1ZJUKC', 'package_name': '十全十美畅享199元套餐（乐享家）', 'detail_name': '乐享家全国上网免4GB（群组共享）', 'detailtotal': '4.0', 'detailremain': '0.0', 'eff_date': '20171001', 'exp_date': '20510101'}, {'package_id': '2-1Y1ZJUKC', 'package_name': '十全十美畅享199元套餐（乐享家）', 'detail_name': '乐享家全国上网免4GB（群组共享）（上月结转）', 'detailtotal': '4.0', 'detailremain': '67.0', 'eff_date': '20171001', 'exp_date': '20510101'}, {'package_id': '2-1RRYD2OY', 'package_name': '爱听4G定向流量（6G）可选包', 'detail_name': '爱听4G包内专用国内上网（含黑莓上网，不含wifi）免6GB', 'detailtotal': '6.0', 'detailremain': '0.0', 'eff_date': '20180927', 'exp_date': '20520801'}, {'package_id': '2-2UL6EMUD', 'package_name': '十全十美套餐0元10G全国流量月包（5个月）', 'detail_name': '国内上网（含黑莓上网，不含wifi）免10GB（群组共享）', 'detailtotal': '10.0', 'detailremain': '0.0', 'eff_date': '20190501', 'exp_date': '20191001'}]

