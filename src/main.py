from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
from config import CONFIG
# from time import sleep
from reptile import LoginYY
from pool import DriverPool
import asyncio



pool = DriverPool(pool_size=3)

async def main():
    # try:
    # 指定Chrome驱动器路径（注意修改为你实际的驱动器路径）
    # driver_path = CONFIG.MAC_ARM64_CHROME
    driver_path = CONFIG.LINUX_64_CHROME
    # print(driver_path)
    # 创建Chrome驱动器服务
    service = Service(driver_path)

    # 创建Chrome浏览器对象
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:

        mainaAcount = CONFIG.MAIN_ACCOUNT
        # loginYY = LoginYY(pool)
        LoginYY.reptile_main_list(driver, mainaAcount['account'], mainaAcount['password'], pool)

    except Exception as e:
        print(e)
        driver.quit()
        await main()

async def init_pool():

    # pass
    
    pool.initialize_pool()

    # 添加任务到任务队列
    pool.add_task('https://www.google.com')
    pool.add_task('https://www.baidu.com')
    pool.add_task('https://cn.aliyun.com')

    # 启动驱动程序池处理任务
    pool.start_pool()


async def run_tasks():
    await asyncio.gather(init_pool(), main())

if __name__ == '__main__':

    asyncio.run(run_tasks())

    # print(11111111111111)
    # main()

    # pool = DriverPool(pool_size=3)
    # pool.initialize_pool()

    # # 添加任务到任务队列
    # pool.add_task('https://www.google.com', 'element1')

    # # 启动驱动程序池处理任务
    # pool.start_pool()
    
    # pool.add_task('https://www.baidu.com', 'element2')
    # pool.add_task('https://chat.openai.com', 'element3')