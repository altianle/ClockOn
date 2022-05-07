# !/user/bin/env python
# -*- coding:utf-8 -*-
# author:ALian  time:2022/5/3

import time
import configparser
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter
from tkinter.messagebox import *
import sys


def getConfig(section, key=None):
    config = configparser.ConfigParser()
    dir = os.path.abspath(".")
    file_path = dir + '\\config.ini'
    config.read(file_path, encoding='utf-8')
    return config.get(section, key)


class PunchCard():
    def __init__(self):
        self.username = getConfig("info", "userName")  # 账号
        self.password = getConfig("info", "passWord")  # 密码

        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        try:
            self.driver = webdriver.Chrome(chrome_options=option)

        except:
            window = tkinter.Tk()
            window.withdraw()
            showerror('错误', '打卡失败：未找到webdriver，请检查路径设置')
            sys.exit(0)
        #self.driver = webdriver.Chrome()
        self.vars = {}

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        self.driver.quit()

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def run(self):
        window = tkinter.Tk()
        window.withdraw()  # 退出默认 tk 窗口
        self.driver.get("http://sso.sut.edu.cn/sso/login?service=http://main.sut.edu.cn/user/simpleSSOLogin")
        self.driver.set_window_size(1920, 1080)

        try:
            self.driver.find_element_by_name("username").send_keys(self.username)
            self.driver.find_element_by_name("password").send_keys(self.password)
            self.driver.find_element(By.CSS_SELECTOR, ".password_arrows").click()
        except:
            showerror('错误', '打卡失败：网页无法打开！')
            return

        time.sleep(3)

        try:
            self.vars["window_handles"] = self.driver.window_handles
            self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(26) img").click()
        except:
            showerror('错误', '打卡失败：账号或密码错误！')
            return

        self.vars["win5084"] = self.wait_for_window(2000)
        self.vars["root"] = self.driver.current_window_handle
        self.driver.switch_to.window(self.vars["win5084"])

        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, ".marT15 > input").send_keys(self.username)
        self.driver.find_element(By.CSS_SELECTOR, ".c-wrap-input:nth-child(4) > input").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, "button").click()

        time.sleep(3)
        target = self.driver.find_element(By.CSS_SELECTOR, ".date-list-item:nth-child(1) > .date-list-item-day")
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        self.driver.find_element(By.CSS_SELECTOR, ".date-list-item:nth-child(1) > .date-list-item-day").click()

        time.sleep(1)
        try:
            target = self.driver.find_element(By.CSS_SELECTOR, ".van-button")
            self.driver.execute_script("arguments[0].scrollIntoView();", target)
            self.driver.find_element(By.CSS_SELECTOR, ".van-button").click()

        except:
            showerror('错误', '已经打过卡！')
            return

        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".van-button").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".van-button").click()

        time.sleep(13)

        try:
            target = self.driver.find_element(By.CSS_SELECTOR, ".submitbtn")
            self.driver.execute_script("arguments[0].scrollIntoView();", target)
            self.driver.find_element(By.CSS_SELECTOR, ".submitbtn").click()

        except:
            showerror('错误', '打卡失败：获取地理信息失败！')
            return

        time.sleep(1)
        showinfo('提示', '打卡成功！')
        # print(f'提示: {result}')

        self.driver.close()
        self.driver.switch_to.window(self.vars["root"])
        self.driver.close()
        self.driver.quit()
        return


if __name__ == '__main__':
    punchcard = PunchCard()
    punchcard.run()
    sys.exit(0)
