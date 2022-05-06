# !/user/bin/env python
# -*- coding:utf-8 -*-
# author:ALian  time:2022/5/3

import time
import configparser
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By


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
        self.driver = webdriver.Chrome()
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
        self.driver.get("http://sso.sut.edu.cn/sso/login?service=http://main.sut.edu.cn/user/simpleSSOLogin")
        self.driver.set_window_size(1920, 1080)
        self.driver.find_element_by_name("username").send_keys(self.username)
        self.driver.find_element_by_name("password").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, ".password_arrows").click()

        time.sleep(3)
        self.vars["window_handles"] = self.driver.window_handles
        self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(26) img").click()
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
        target = self.driver.find_element(By.CSS_SELECTOR, ".van-button")
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        self.driver.find_element(By.CSS_SELECTOR, ".van-button").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".van-button").click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".van-button").click()

        time.sleep(13)
        target = self.driver.find_element(By.CSS_SELECTOR, ".submitbtn")
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        self.driver.find_element(By.CSS_SELECTOR, ".submitbtn").click()


        time.sleep(5)
        self.driver.close()
        self.driver.switch_to.window(self.vars["root"])
        self.driver.close()


if __name__ == '__main__':
    punchcard = PunchCard()
    punchcard.run()
