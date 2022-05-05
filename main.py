# !/user/bin/env python
# -*- coding:utf-8 -*-
# author:ALian  time:2022/5/3


import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class PunchCard():
    def __init__(self):
        self.username = ""  # 账号
        self.password = ""  # 密码

        path = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver'  # webdriver路径，需要放在Chrome/Application下
        self.driver = webdriver.Chrome(executable_path=path)
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
        target = self.driver.find_element(By.CSS_SELECTOR, ".submitbtn")
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        self.driver.find_element(By.CSS_SELECTOR, ".submitbtn").click()

        # 电脑有时候需要手动定位
        time.sleep(100)
        self.driver.close()
        self.driver.switch_to.window(self.vars["root"])
        self.driver.close()


if __name__ == '__main__':
    punchcard = PunchCard()
    punchcard.run()
