from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, JavascriptException
from time import sleep
import time
import json
from getSerInfo import getJFQTinfo
from universal import UniversalModel

CTC_URL = 'https://www.xx.xxx.com/'
JFQT_URL = 'http://www.xx.xxx.com/xxxx/xxxxxxxxxxx/xxLoginCmd.go'


class LoginCtc(object):

    def __init__(self, driver):
        driver.maximize_window()
        driver.get(CTC_URL)
        um = UniversalModel()
        self.__user = um.readUser()
        self.__password = um.readPassword()
        try:
            dynamic = driver.find_element(By.CLASS_NAME, "dynamic")
            dynamic.click()
        except WebDriverException as e:
            try:
                okbtn = driver.find_element(By.ID, "okButton")
                WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "okButton")))
                okbtn.click()
            except WebDriverException as e:
                WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.ID, "tipsButton")))
                driver.find_element(By.ID, "tipsButton").click()
            finally:
                driver.find_element(By.CLASS_NAME, "dynamic").click()
        finally:
            self.__login(driver)

    def __login(self, driver):
        username = driver.find_element(By.ID, "m_userid")
        username.clear()
        username.send_keys(self.__user)

        password = driver.find_element(By.ID, "m_password")
        password.clear()
        password.send_keys(self.__password)

        sms = driver.find_element(By.ID, "sendsms")
        sms.click()

        try:
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'content')))
        except TimeoutException:
            self.__login(driver)


class QueryJFQT(object):
    def __init__(self, driver):
        self.driver = driver
        self.__FIRST = True
        self.__comObj = self.__readComObj()

    def __readComObj(self):
        config = {}
        try:
            with open('sec.json', 'rb') as file:
                config = json.load(file)
        except json.JSONDecodeError:
            pass
        return config['compare_obj']

    def __getJFQT(self):
        """
        进入计费前台界面
        :return:
        """
        self.driver.get(JFQT_URL)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.NAME, 'login_in')))
        except TimeoutException as e:
            print(str(time.localtime()) + "," + str(e))
        choose = self.driver.find_element(By.NAME, 'login_in')
        self.driver.execute_script("arguments[0].click();", choose)
        self.__jfqt = self.driver.current_window_handle

    def __getOneStop(self):
        """
        进入一站式页面
        :return:
        """
        sleep(1)
        WebDriverWait(self.driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, 'all_top')))

        # nav = self.driver.find_element_by_link_text("一站式导航")
        # nav.click()
        # nav.send_keys(Keys.ENTER)

        # nav = self.driver.find_element_by_link_text("一站式导航")
        # ActionChains(self.driver).move_to_element(nav).click(nav).perform()

        # nav = self.driver.find_element(By.CSS_SELECTOR, '#top10>a')
        # nav.click()
        sleep(1)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#top10>a')))
        try:
            js = "javascript:do_click(10)"
            self.driver.execute_script(js)
        except JavascriptException:
            nav = self.driver.find_element(By.CSS_SELECTOR, '#top10>a')
            nav.click()

        # self.driver.execute_script("arguments[0].click();", nav)

        self.driver.switch_to.default_content()
        sleep(3)
        self.__switchWindow('账务一站式导航系统')

    def queryValue(self, value, if_ser=True):
        if self.__FIRST:
            self.__FIRST = False
            self.__getJFQT()
        self.__currentIfJFQT()
        self.__getOneStop()
        if if_ser:
            self.__enterMainMenu(value)
        else:
            self.__enterMainMenu(value, if_ser=False)
        return self.__getPageSource()

    def __currentIfJFQT(self):
        """
        判断当前窗口是否时计费前台界面，如果不是就切换当前窗口到计费前台
        :return:
        """
        if self.driver.current_window_handle != self.__jfqt:
            self.driver.close()
            self.driver.switch_to.window(self.__jfqt)
            self.driver.maximize_window()

    def __enterMainMenu(self, value, if_ser=True):
        if if_ser:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'device_no')))
            inv = self.driver.find_element(By.ID, "device_no")
            inv.clear()
            inv.send_keys(value)

            nav = self.driver.find_element(By.XPATH, "//ul[@class='zd_content']/li[1]/p/input[1]")
            nav.click()

            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'calendarPanel')))
            except TimeoutException:
                acctpath = "//table[@class='contentta']/tbody/tr[1]/td[1]/a"
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, acctpath)))
                acct = self.driver.find_element(By.XPATH, acctpath)
                acct.click()

        else:
            acct_btn = self.driver.find_element(By.XPATH, "//div[@class='bg png_bg']/ul/li[2]")
            acct_btn.click()
            inv = self.driver.find_element(By.ID, "account_no")
            inv.clear()
            inv.send_keys(value)

            nav = self.driver.find_element(By.XPATH, "//ul[@class='zd_content']/li[2]/p/input[1]")
            nav.click()

    def __getPageSource(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'tt')))
        sleep(1)
        bundleinfo = ''
        userinfo = ''
        if '1' in self.__comObj:
            bundlebtn = self.driver.find_element(By.ID, 'accountLevel').find_element(By.XPATH, "//div\
                [@class='tabs-header']/div[@class='tabs-wrap']/ul/li[3]/a")
            self.driver.execute_script("arguments[0].click();", bundlebtn)
            sleep(1)
            WebDriverWait(self.driver, 15).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'datagrid-mask-msg')))
            bundleinfo = self.driver.page_source
        if '2' in self.__comObj:
            useinfobtn = self.driver.find_element(By.ID, 'accountLevel').find_element(By.XPATH, "//div\
                [@class='tabs-header']/div[@class='tabs-wrap']/ul/li[13]/a")
            self.driver.execute_script("arguments[0].click();", useinfobtn)
            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "cqdUsedInfo")))
            # self.driver.switch_to.frame(self.driver.find_element(By.ID, 'cqdUsedInfo'))
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div\
                [@id='freeMsgPanel']/div[@class='panel datagrid']/div[@class='panel-header']")))
            userinfo = self.driver.page_source
        self.driver.switch_to.default_content()

        return [bundleinfo, userinfo]

    def __switchWindow(self, title):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if self.driver.title == title:
                break
        # self.driver.switch_to.window(self.driver.window_handles[-1])

if __name__ == '__main__':

    driver = webdriver.Ie()
    LoginCtc(driver)
    search = QueryJFQT(driver)
    a, b = search.queryValue('')
    print(getJFQTinfo(a).getBundleinfo())
    print(getJFQTinfo(b).getUseInfoCqd())
    # search.queryValue('15300510610')

    # ser_list = ['', '', '', '', '']
    # for ser in ser_list:
    #     a, b = search.queryValue(ser)
    #     print(getJFQTinfo(a).getBundleinfo())

    driver.quit()





