import os;
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from oss import upload
from dingAlarm import sendDingMsg
import unittest
import time
import sys
from lib import log
from config import webInfo

#TODO: 测试报告


class TestLogin(unittest.TestCase):
    # 模拟前准备
    def setUp(self):
        driverPath = os.path.abspath('chromedriver')
        webaddr = webInfo['addr']

        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        self.driver = Chrome(driverPath, options=option)

        self.driver.get(webaddr)
        #模拟登录账号
        self.account = webInfo['account']
        #模拟登录密码
        self.password = webInfo['password']
        #图片上传oss的地址
        self.ossPath = webInfo['ossPath']
        #图片的cdn域名
        self.cdnHost = webInfo['cdnHost']
        #若有错误，截图后图片的本地的地址
        self.localImgList = []
        #若有错误，截图并上传到oss后，oss的地址
        self.ossImgList = []
        log('网址已打开:  ' + webaddr + '。现在登录, 账号: ' + self.account + ', 密码: ' + self.password);
    

    #删除文件夹
    def removeFile(self, fileName):
        if(os.path.exists(fileName)):
            os.remove(fileName)

    #根据传入文件名，获取要上传到oss的路径
    def getOssPath(self, fileName):
        localtime = time.strftime("%Y%m%d", time.localtime())
        ossPath = self.ossPath + str(localtime) + '/'
        return ossPath + fileName

    #根据dingAlarm库要求的发钉钉消息的格式制造json
    def createDingMessageJson(self, title, subtitle, imgList):
        messageJson = {}
        messageJson['title'] = title;
        messageJson['lines'] = [];
        messageJson['lines'].append({'type':'text', 'fontSize': '#', 'content': title})
        messageJson['lines'].append({'type':'text', 'style': '>', 'fontSize': '###', 'content': subtitle})
        messageJson['lines'].append({'type':'text', 'style': '>', 'fontSize': '#####', 'content': '模拟登录账号: ' + self.account})
        messageJson['lines'].append({'type':'text', 'style': '>', 'fontSize': '#####', 'content': '模拟登录密码: ' + self.password})
        messageJson['lines'].append({'type':'text', 'style': '>', 'fontSize': '######', 'content': '截图如下'})
        messageJson['lines'].append({'type':'img',  'style': '>', 'urls': imgList})
        return messageJson;

    #截图，并且把图片上传到oss
    def captureAndUpload(self, imgName):
        localtime = str(time.strftime("%H%M%S", time.localtime()))
        homeImgName = imgName + '_' + localtime + '.png'        
        self.driver.save_screenshot(homeImgName)
        localImg = os.path.abspath(homeImgName)
        self.localImgList.append(localImg)
        ossPath = self.getOssPath(homeImgName)
        fullOssPath = self.cdnHost + '/' + ossPath
        self.ossImgList.append(fullOssPath)
        upload(ossPath, localImg)
        log('异常截图已上传: ' + fullOssPath);


    # 登录的测试用例
    def test_login(self):
        try:
            #输入账号密码
            accountInput = self.driver.find_element_by_id("j-phone-normal-input")
            accountInput.send_keys(self.account)
            pswInput = self.driver.find_element_by_id("j-password-normal-input")
            pswInput.send_keys(self.password)
            #输入回车
            pswInput.send_keys(Keys.RETURN)

            try:
                #输入账号密码登录后，看下错误弹窗有无出来
                WebDriverWait(self.driver, 2).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "xh-message"))
                    )
                #如果有出来，截图，并且发钉钉消息
                log('发现异常');
                self.captureAndUpload('error');
                sendDingMsg(self.createDingMessageJson(title='天幕管理后台前端监控', subtitle='登录测试未通过', imgList=self.ossImgList))

            except:
                #如果没有出来，检查进入主页后有无class为org-list的元素（页面是否正常加载）
                WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "org-list"))
                    )

        except:
            #若报错，截图，发钉钉消息
            log('发现异常');
            self.captureAndUpload('error')
            sendDingMsg(self.createDingMessageJson(title='天幕管理后台前端监控', subtitle='登录测试未通过', imgList=self.ossImgList))
            


    # 关闭浏览器
    def tearDown(self):
        self.driver.quit()
        #删除本地图片
        for img in self.localImgList:
            self.removeFile(img)




if __name__ == "__main__":
    unittest.main();