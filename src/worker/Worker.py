import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from config import CONFIG
from reptile import LoginYY
import json
import asyncio




class Worker(threading.Thread):

    def __init__(self):
        super().__init__()
        self.drives = {}
        self.is_running = True
        self.use_drivers = {}

    async def run_async(self):
        # try:
        # 指定Chrome驱动器路径（注意修改为你实际的驱动器路径）
        driver_path = CONFIG.MAC_ARM64_CHROME
        # driver_path = CONFIG.LINUX_64_CHROME
        # print(driver_path)
        # 创建Chrome驱动器服务
        service = Service(driver_path)

        # 创建Chrome浏览器对象

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        accounts = CONFIG.SUB_ACCOUNT

        for account in accounts:
            loginYY = LoginYY()
            loginYY.login_yy(driver, account['account'], account['password'])

            self.drives[f"{account['account']}:{account['password']}"] = driver

    def run(self):
        self.reptile_sub_data()
        asyncio.run(self.run_async())

    def reptile_sub_data(self):
        while self.is_running:
            for key, drive in self.drives.items():
                if key not in self.use_drivers:
                    loginYY = LoginYY()
                    loginYY.reptile_detail_data(url)
            pass

    def stop(self):
        self.is_running = False
