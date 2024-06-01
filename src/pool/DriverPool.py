from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from multiprocessing.dummy import Pool as ThreadPool
import time
from config import CONFIG
from reptile import LoginYY
# from reptile.LoginYY import LoginYY



class DriverPool:
    def __init__(self, pool_size=5):
        self.pool_size = pool_size
        self.drivers = []
        self.tasks = []

    def create_driver(self, account, password):
        service = Service(CONFIG.MAC_ARM64_CHROME)
        # service = Service(CONFIG.LINUX_64_CHROME)
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=service, options=chrome_options)  # 这里可以根据需要选择其他浏览器驱动
        try:
        # if 1 == 1:
            # loginYY = LoginYY()
            LoginYY.login_yy(driver, account, password)

            # self.drives[f"{account['account']}:{account['password']}"] = driver

            self.drivers.append(driver)
        except Exception as e:
            print(e)
            driver.quit()
            self.create_driver(account=account, password=password)

    def initialize_pool(self):
        accounts = CONFIG.SUB_ACCOUNT
        size = self.pool_size if len(accounts) > self.pool_size else len(accounts)
        print(f'客户端数量{size}')
        for index in range(size):
            print(f'客户端{index}')
            account = accounts[index]
            self.create_driver(account['account'], account['password'])

    def execute_task(self, url, driver):
        print('执行详情请求')
        # driver = self.drivers.pop()
        try:
            # driver.get(url)
            # # 在这里可以添加其他的爬虫任务逻辑，例如查找元素、获取数据等
            # # 这里仅作示例，具体任务逻辑根据实际情况修改
            # print(f"任务完成: {url}")
            # # self.tasks.remove(url)
            # print(self.tasks)

            LoginYY.reptile_detail_data(driver, url)
        except Exception as e:
            print(f"任务失败: {url}, 错误: {e}")
        finally:
            print('重新添加到全局drivers里面')
            self.drivers.append(driver)
            print(self.drivers)

    def add_task(self, url):
        print(f'添加url{url}')
        self.tasks.append(url)

    def start_pool(self):
        with ThreadPoolExecutor(max_workers=self.pool_size) as executor:
            while len(self.tasks) > 0:
                if len(self.drivers) > 0:
                    url = self.tasks.pop(0)
                    driver = self.drivers.pop(0)
                    executor.submit(self.execute_task, url, driver)
                # for driver in self.drivers:
                #     if self.tasks:
                #         url = self.tasks.pop(0)
                #         executor.submit(self.execute_task, url, driver)

    