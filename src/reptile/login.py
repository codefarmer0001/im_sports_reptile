
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from config import CONFIG
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import re
import time


import base64
from io import BytesIO
from aip import AipOcr
import os

from myredis import produce, consumer, redis_util

from logs import getLogger  # 导入日志配置模块
logger = getLogger('list')

mode = os.environ.get('MODE', 'DEV')


class login:


    @staticmethod
    def main():
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
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--disable-extensions')
        # chrome_options.add_argument('--start-maximized')
        # chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.page_load_strategy = 'none'
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver.implicitly_wait(5)  # 设置全局隐式等待时间为5秒
        try:

            mainaAcount = CONFIG.MAIN_ACCOUNT
            print(mainaAcount)
            login.reptile_main_list(driver, mainaAcount['account'], mainaAcount['password'])
                

        except Exception as e:
            print(e)
            driver.quit()
            login.main()

    
    @staticmethod
    def reptile_main_list(driver, account, password):
    # def reptile_main_list(self, driver, account, password, pool):
        login.login_account(driver, account, password)

        r = redis_util()
        r.set_string(mode, time.time())

        creator = produce()
        creator.push_list(CONFIG.IM_REPTILE_FLAG)
        consumer(driver, creator, r)
        sleep(3600)

    
    @staticmethod
    def login_account(driver, account, password):
    # def login_yy(self, driver, account, password):
        print(f'driver获取内容：{driver}')
        start_time = time.time()
        driver.get(CONFIG.YY_MAIN_URL)
        print(f'driver加载页面耗时：{time.time() - start_time}')
        print(CONFIG.YY_MAIN_URL)

        wait = WebDriverWait(driver, 10, poll_frequency=0.1)

        # try:
        if 1 == 1:
            login_btn_panl = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'login_menu'))
            )

            login_button = login_btn_panl.find_element(By.XPATH, '//button[@class="login_btn"]')

            driver.execute_script("arguments[0].click();", login_button)


            # print(login_btn_panl)


            login_panl = wait.until(
                EC.visibility_of_element_located((By.ID, 'loginModal'))
            )

            input_user_name = login_panl.find_element(By.ID, 'account')
            input_password = login_panl.find_element(By.ID, 'pwd')
            input_inputcode = login_panl.find_element(By.ID, 'inputcode')

            # 等待元素加载
            img_code = wait.until(lambda driver: driver.find_element(By.ID, 'pic').get_attribute('src') != '')
            img_code = login_panl.find_element(By.ID, 'pic')
            src_value = img_code.get_attribute('src')
            
            # print(src_value)

            # 将 Base64 数据解码为字节流
            image_data = base64.b64decode(src_value.replace('data:image/jpeg;base64,', ''))

            # 读取字节流为 PIL 图像对象
            # image = Image.open(BytesIO(image_data))

            # 使用 BytesIO 将图像数据转换为文件对象
            image_file = BytesIO(image_data)

            # 读取文件对象中的数据
            content = image_file.read()

            # 保存图像为 PNG 格式
            # image.save("output.png", "PNG")

            client = AipOcr(CONFIG.BAIDU_APP_ID, CONFIG.BAIDU_API_KEY, CONFIG.BAIDU_SECRET_KEY)

            # 调用通用文字识别（标准版）
            res_image = client.basicGeneral(content)

            result = dict(res_image)
            code = result['words_result'][0]['words']
            code = re.sub(r"\s+", "", code)

            pattern = r'^[A-Za-z0-9]{4}$'

            if bool(re.match(pattern, code)):

                input_user_name.send_keys(account)
                input_password.send_keys(password)
                input_inputcode.send_keys(code.lower().replace('.', '').replace(':', '').replace('\'', ''))

                print(code)

                # 使用 execute_script 调用 JavaScript 的 SubmitLogin() 方法
                driver.execute_script("SubmitLogin();")

                try:

                    notice_panl = wait.until(
                        EC.visibility_of_element_located((By.ID, 'focus_announce'))
                    )
                    # cancel
                    if notice_panl:
                        notice_calcel = notice_panl.find_element(By.XPATH, './/button[@class="cancel"]')
                        driver.execute_script("arguments[0].click();", notice_calcel)

                except Exception as e:
                    print('公告界面可能不存在')

                game_panal = wait.until(
                    EC.visibility_of_element_located((By.XPATH, './/ul[@class="recreation_list active"]'))
                )

                if game_panal:
                    game_list = game_panal.find_elements(By.XPATH, './/div[@class="platform_info"]')
                    if game_list:
                        # print(game_list)
                        for item in game_list:
                            platform_name = item.find_element(By.CLASS_NAME, 'platform')
                            platform_name_text = platform_name.get_attribute('innerHTML')
                            # print(platform_name)
                            # print(platform_name_text)
                            if 'IM体育' == platform_name_text:
                                driver.execute_script("arguments[0].click();", item)
                                break
                
                sport_dialog = wait.until(
                    EC.visibility_of_element_located((By.ID, 'Modal_sports'))
                )
                
                cancel_order = sport_dialog.find_element(By.ID, 'cancel_order')
                driver.execute_script("arguments[0].click();", cancel_order)

                handles = driver.window_handles
                driver.switch_to.window(handles[1])  # 切换到第二个标签页（索引从0开始）

                action_chains = ActionChains(driver)
                flag = True
                index = 0
                try:
                    bg_mask = None
                    try:
                        bg_mask = wait.until(
                            EC.visibility_of_element_located((By.CLASS_NAME, 'bg_mask'))
                        )
                    except Exception as e:
                        bg_mask = None
                    
                    print(34567)
                    if bg_mask:
                        while flag:
                        # mask_button rc_tut_btn
                            mask_button = bg_mask.find_element(By.XPATH, './/div[@class="mask_button rc_tut_btn"]')
                            print(111111111)
                            if mask_button:
                                index += 1
                                action_chains.move_to_element(mask_button).perform()
                                driver.execute_script("arguments[0].click();", mask_button)
                            else:
                                flag = False
                except Exception as e:
                    flag = False
                    print("元素失效，请重新定位或等待一段时间后重试")

            else:
                driver.quit()
                login.main()
                # sleep(3600)