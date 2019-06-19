from universal import UniversalModel
from copy import deepcopy


class Compare(object):
    def __init__(self, service_nbr):
        self.__service_nbr = service_nbr
        self.__path = UniversalModel().read_file_path()

    def bundleDataCompare(self, weblist, oraclelist):
        if len(weblist) != len(oraclelist):
            with open(self.__path, 'a', encoding='UTF-8') as file:
                file.write(self.__service_nbr+'\n'+str(weblist)+"\n"+str(oraclelist)+"\n")
            return self.__service_nbr
        else:
            orlength = len(oraclelist)
            ororaclelist = deepcopy(oraclelist)
            if orlength:
                for web in weblist:
                    for index, oracle in enumerate(oraclelist):
                        if self.__valueEqual(web, oracle):
                            oraclelist.pop(index)
                            orlength -= 1
                            break
                        elif index == orlength - 1:
                            with open(self.__path, 'a', encoding='UTF-8') as file:
                                file.write(self.__service_nbr + '\n' + str(weblist) + "\n" + str(ororaclelist) + "\nbundle" + str(web) + "\nora" + str(oracle) + "\n")
                            return self.__service_nbr
            return None

    def __valueEqual(self, web, oracle):
        # if web['package_id'] != oracle['package_id']:
        #     return False
        if web['package_name'] != oracle['package_name']:
            return False
        if web['detail_name'] != oracle['detail_name']:
            return False
        if float(web['detailtotal']) != float(oracle['detailtotal']):
            return False
        if float(web['detailremain']) != float(oracle['detailremain']):
            if float(web['detailremain']) + 0.01 != float(oracle['detailremain']):
                return False
        # if web['eff_date'] != oracle['eff_date']:
        #     return False
        # if web['exp_date'] != oracle['exp_date']:
        #     return False
        return True

    def cqdDataCompare(self, cqdlist, oraclelist):
        if len(cqdlist) != len(oraclelist):
            with open(self.__path, 'a', encoding='UTF-8') as file:
                file.write(self.__service_nbr+'\n'+str(cqdlist)+"\n"+str(oraclelist)+"\n")
            return self.__service_nbr
        else:
            orlength = len(oraclelist)
            ororaclelist = deepcopy(oraclelist)
            if orlength:
                for cqd in cqdlist:
                    for index, oracle in enumerate(oraclelist):
                        if self.__cqdvalueEqual(cqd, oracle):
                            oraclelist.pop(index)
                            orlength -= 1
                            break
                        elif index == orlength - 1:
                            with open(self.__path, 'a', encoding='UTF-8') as file:
                                file.write(self.__service_nbr + '\n' + str(cqdlist) + "\n" + str(ororaclelist) + "\ncqd:" + str(cqd)+ "\nora:" + str(oracle) + "\n")
                            return self.__service_nbr
            return None

    def __cqdvalueEqual(self, web, oracle):
        if web['package_id'] != oracle['package_id']:
            return False
        if web['package_name'] != oracle['package_name']:
            return False
        if web['detail_name'] != oracle['detail_name']:
            return False
        if float(web['detailtotal']) != float(oracle['detailtotal']):
            return False
        if float(web['detailremain']) != float(oracle['detailremain']):
            if float(web['detailremain']) + 0.01 != float(oracle['detailremain']):
                return False
        # if web['eff_date'] != oracle['eff_date']:
        #     return False
        # if web['exp_date'] != oracle['exp_date']:
        #     return False
        return True

if __name__ == '__main__':
    cqd = [{'package_id': '2-1QNLPDCG', 'package_name': '宽带网龄赠送0元800M+800M闲时国内流量包',
            'detail_name': '国内上网（含黑莓上网，不含wifi）免800MB', 'detailtotal': 800.0, 'detailremain': 746.29,
            'eff_date': '20190501000000', 'exp_date': '20190531235959'},
           {'package_id': '2-1QNLPDCG', 'package_name': '宽带网龄赠送0元800M+800M闲时国内流量包',
            'detail_name': '国内上网（含黑莓上网，不含wifi）免800MB（晚23点到早7点）', 'detailtotal': 800.0, 'detailremain': 76.0,
            'eff_date': '20190501000000', 'exp_date': '20190531235959'},
           {'package_id': '2-1RRYD2OY', 'package_name': '爱听4G定向流量（6G）可选包',
            'detail_name': '爱听4G包内专用国内上网（含黑莓上网，不含wifi）免6GB', 'detailtotal': 6.0, 'detailremain': 0.0,
            'eff_date': '20190501000000', 'exp_date': '20190531235959'},
           {'package_id': '2-1W35KMMW', 'package_name': '0元40GB国内达量降速可选包',
            'detail_name': '国内上网（含黑莓上网，不含wifi）免40GB（群组共享）', 'detailtotal': 40.0, 'detailremain': 2.59,
            'eff_date': '20190501000000', 'exp_date': '20190531235959'},
           {'package_id': '2-1Y1ZJUKC', 'package_name': '十全十美畅享199元套餐（乐享家）', 'detail_name': '乐享家全国上网免4GB(群组共享)(上月结转)',
            'detailtotal': 4.0, 'detailremain': 67.0, 'eff_date': '20190501000000', 'exp_date': '20190531235959'},
           {'package_id': '2-1Y1ZJUKC', 'package_name': '十全十美畅享199元套餐（乐享家）', 'detail_name': '乐享家全国上网免4GB（群组共享）',
            'detailtotal': 4.0, 'detailremain': 0.0, 'eff_date': '20190501000000', 'exp_date': '20190531235959'},
           {'package_id': '2-2UL6EMUD', 'package_name': '十全十美套餐0元10G全国流量月包（5个月）',
            'detail_name': '国内上网（含黑莓上网，不含wifi）免10GB（群组共享）', 'detailtotal': 10.0, 'detailremain': 0.0,
            'eff_date': '20190501000000', 'exp_date': '20190531235959'},
           {'package_id': '2-XIKXDFW', 'package_name': '2014年员工套餐WIFI时长包', 'detail_name': '国内wifi上网免120小时',
            'detailtotal': '7200', 'detailremain': '0分钟', 'business_type': '分钟', 'eff_date': '20190501000000',
            'exp_date': '20190531235959'}]

    oracle = [{'package_id': '2-XIKXDFW', 'package_name': '2014年员工套餐WIFI时长包', 'detail_name': '国内wifi上网免120小时',
            'detailtotal': '7200', 'detailremain': '0', 'eff_date': '20171001', 'exp_date': '20510101'},
           {'package_id': '2-1QNLPDCG', 'package_name': '宽带网龄赠送0元800M+800M闲时国内流量包',
            'detail_name': '国内上网（含黑莓上网，不含wifi）免800MB', 'detailtotal': '800.0', 'detailremain': '800.0',
            'eff_date': '20170301', 'exp_date': '20501230'},
           {'package_id': '2-1QNLPDCG', 'package_name': '宽带网龄赠送0元800M+800M闲时国内流量包',
            'detail_name': '国内上网（含黑莓上网，不含wifi）免800MB（晚23点到早7点）', 'detailtotal': '800.0', 'detailremain': '76.0',
            'eff_date': '20170301', 'exp_date': '20501230'},
           {'package_id': '2-1W35KMMW', 'package_name': '0元40GB国内达量降速可选包',
            'detail_name': '国内上网（含黑莓上网，不含wifi）免40GB（群组共享）', 'detailtotal': '40.0', 'detailremain': '2.59',
            'eff_date': '20171001', 'exp_date': '20500102'},
           {'package_id': '2-1Y1ZJUKC', 'package_name': '十全十美畅享199元套餐（乐享家）', 'detail_name': '乐享家全国上网免4GB（群组共享）',
            'detailtotal': '4.0', 'detailremain': '0.0', 'eff_date': '20171001', 'exp_date': '20510101'},
           {'package_id': '2-1Y1ZJUKC', 'package_name': '十全十美畅享199元套餐（乐享家）', 'detail_name': '乐享家全国上网免4GB（群组共享）（上月结转）',
            'detailtotal': '4.0', 'detailremain': '67.0', 'eff_date': '20171001', 'exp_date': '20510101'},
           {'package_id': '2-1RRYD2OY', 'package_name': '爱听4G定向流量（6G）可选包',
            'detail_name': '爱听4G包内专用国内上网（含黑莓上网，不含wifi）免6GB', 'detailtotal': '6.0', 'detailremain': '0.0',
            'eff_date': '20180927', 'exp_date': '20520801'},
           {'package_id': '2-2UL6EMUD', 'package_name': '十全十美套餐0元10G全国流量月包（5个月）',
            'detail_name': '国内上网（含黑莓上网，不含wifi）免10GB（群组共享）', 'detailtotal': '10.0', 'detailremain': '0.0',
            'eff_date': '20190501', 'exp_date': '20191001'}]

    a = Compare('13311802892')
    a.cqdDataCompare(cqd, oracle)
