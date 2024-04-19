from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from config import CONFIG
from time import sleep
from reptile import LoginYY


def main():
    # try:
    # 指定Chrome驱动器路径（注意修改为你实际的驱动器路径）
    driver_path = CONFIG.MAC_ARM64_CHROME
    # print(driver_path)
    # 创建Chrome驱动器服务
    service = Service(driver_path)

    # 创建Chrome浏览器对象
    driver = webdriver.Chrome(service=service)
    try:
        loginYY = LoginYY()
        loginYY.login_yy(driver)
    except Exception as e:
        print(e)
        driver.quit()
        main()
        # loginYY = LoginYY()
        # loginYY.login_yy()

if __name__ == '__main__':

    main()
    