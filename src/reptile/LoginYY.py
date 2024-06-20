
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from config import CONFIG
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.common.exceptions import StaleElementReferenceException
import time
import re
import asyncio
from bs4 import BeautifulSoup
import requests

import base64
from PIL import Image
from io import BytesIO
from aip import AipOcr

from myredis import produce, consumer

from logs import getLogger  # 导入日志配置模块
logger = getLogger('list')


# from pool import DriverPool

class LoginYY:

    # def __init__(self, pool = None) -> None:
    #     if pool:
    #         self.pool = pool
    #     pass

    @staticmethod
    def get_file_content(filePath):
        with open(filePath, "rb") as fp:
            return fp.read()
    
    @staticmethod
    def login_yy(driver, account, password):
    # def login_yy(self, driver, account, password):
        
        # 打开网页
        # url = 'https://o3q.mltyz6.com/'

        driver.get(CONFIG.YY_MAIN_URL)
        print(CONFIG.YY_MAIN_URL)

        # try:
        if 1 == 1:
            login_btn_panl = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'login_menu'))
            )

            login_button = login_btn_panl.find_element(By.XPATH, '//button[@class="login_btn"]')
            # print(login_button.text)
            # login_button.click()
            driver.execute_script("arguments[0].click();", login_button)


            print(login_btn_panl)


            login_panl = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.ID, 'loginModal'))
            )

            input_user_name = login_panl.find_element(By.ID, 'account')
            input_password = login_panl.find_element(By.ID, 'pwd')
            input_inputcode = login_panl.find_element(By.ID, 'inputcode')

            # 创建 WebDriverWait 对象
            wait = WebDriverWait(driver, 10)

            # 等待元素加载
            img_code = wait.until(lambda driver: driver.find_element(By.ID, 'pic').get_attribute('src') != '')
            img_code = login_panl.find_element(By.ID, 'pic')
            src_value = img_code.get_attribute('src')
            
            print(src_value)

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


            input_user_name.send_keys(account)
            input_password.send_keys(password)
            input_inputcode.send_keys(code.replace('.', '').replace(':', '').replace('\'', ''))

            print(code)

            # 使用 execute_script 调用 JavaScript 的 SubmitLogin() 方法
            driver.execute_script("SubmitLogin();")

            try:

                notice_panl = WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.ID, 'focus_announce'))
                )
                # cancel
                if notice_panl:
                    notice_calcel = notice_panl.find_element(By.XPATH, './/button[@class="cancel"]')
                    driver.execute_script("arguments[0].click();", notice_calcel)

            except Exception as e:
                print('公告界面可能不存在')

            game_panal = WebDriverWait(driver, 15).until(
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
            
            sport_dialog = WebDriverWait(driver, 15).until(
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
                    bg_mask = WebDriverWait(driver, 10).until(
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

            # sleep(3600)



        # except Exception as e:
        #     print(e)


        # # try:
        # if 1 == 1:
        #     element = WebDriverWait(driver, 10).until(
        #         EC.visibility_of_element_located((By.CLASS_NAME, 'buttons'))
        #     )
        #     # 登陆界面，打开登陆dialog
        #     # print(element)
        #     login_button = element.find_element(By.XPATH, '//button[@class="el-button el-button--primary login"]')
        #     # print(login_button.text)
        #     # login_button.click()
        #     driver.execute_script("arguments[0].click();", login_button)
        #     # print(111111111)

        #     # pane-account
        #     login_panel = WebDriverWait(driver, 10).until(
        #         EC.visibility_of_element_located((By.ID, 'pane-account'))
        #     )
        #     # print(login_panel)
        #     input_user_name = login_panel.find_element(By.XPATH, '//input[@placeholder="请输入用户名"]')
        #     # print(input_user_name)
        #     input_user_name.send_keys(account)

        #     input_password = login_panel.find_element(By.XPATH, '//input[@placeholder="请输入密码"]')
        #     # print(input_password)
        #     input_password.send_keys(password)

        #     login_panal_submit = login_panel.find_element(By.XPATH, '//button[@type="submit"]')
        #     # print(login_panal_submit)
        #     # login_panal_submit.click()
        #     driver.execute_script("arguments[0].click();", login_panal_submit)
        #     # print(111111111)

        #     # 主界面，登陆完后的界面

        #     main_panal_dialog = WebDriverWait(driver, 10).until(
        #         EC.visibility_of_element_located((By.CLASS_NAME, 'home-act-dialog'))
        #     )
        #     main_panal_dialog_close = main_panal_dialog.find_element(By.XPATH, '//button[@type="button" and @aria-label="Close"]')
        #     # print(main_panal_dialog_close)
        #     driver.execute_script("arguments[0].click();", main_panal_dialog_close)
        #     # print(111111111)
        #     # main_panal_dialog_close.click()


        #     # # navbar选项
        #     main_panal_navbar = WebDriverWait(driver, 10).until(
        #         EC.visibility_of_element_located((By.CLASS_NAME, 'navbar'))
        #     )
        #     sport_items = main_panal_navbar.find_element(By.XPATH, './/li[@class="sport"]')
        #     # print('\n\n\n')
        #     # print(sport_items.get_attribute('outerHTML'))

        #     sport_items_lable = sport_items.find_element(By.XPATH, './/span[@class="label"]')

        #     # sport_items.click()
        #     # 创建 ActionChains 对象
        #     action_chains = ActionChains(driver)

        #     # print('\n\n\n')
        #     # print(sport_items_lable.get_attribute('outerHTML'))
        #     # print('\n\n\n')

        #     # # 将鼠标移动到元素上
        #     action_chains.move_to_element(sport_items_lable).perform()

        #     sport_swiper = sport_items.find_element(By.XPATH, './/div[@class="swiper-wrapper"]')
        #     # print(sport_swiper.get_attribute('outerHTML'))

        #     try:
        #         sport_swiper_items = sport_swiper.find_elements(By.XPATH, './/div[@class="plat"]')
        #         # print(sport_swiper_items)
        #         if sport_swiper_items:
        #             for item in sport_swiper_items:
        #                 # print('\n\n\n')
        #                 # print(123123)
        #                 # print(item.get_attribute('outerHTML'))
        #                 # print('\n\n\n')
        #                 item_span = item.find_element(By.XPATH, './/span')
        #                 # print(item_span.get_attribute('innerHTML'))
        #                 txt = item_span.get_attribute('innerHTML')
        #                 if txt == 'IM体育':
        #                     next = sport_items.find_element(By.XPATH, './/div[@aria-label="Next slide" and @aria-disabled="false"]')
        #                     # print(next.is_enabled())
        #                     action_chains.move_to_element(next).perform()
        #                     driver.execute_script("arguments[0].click();", next)

        #                     taget_item = item.find_element(By.XPATH, './/div[@class="main-pic"]')
        #                     action_chains.move_to_element(taget_item).perform()
        #                     driver.execute_script("arguments[0].click();", taget_item)
        #     except Exception as e:
        #         print(e)
            
        #     print(111111111)
        #     # 切换到新标签页
        #     handles = driver.window_handles
        #     driver.switch_to.window(handles[1])  # 切换到第二个标签页（索引从0开始）

        #     action_chains = ActionChains(driver)
        #     flag = True
        #     index = 0
        #     try:
        #     # if 1 == 1:
        #         bg_mask = None
        #         try:
        #             bg_mask = WebDriverWait(driver, 10).until(
        #                 EC.visibility_of_element_located((By.CLASS_NAME, 'bg_mask'))
        #             )
        #         except Exception as e:
        #             bg_mask = None
                
        #         print(34567)
        #         if bg_mask:
        #             while flag:
        #             # mask_button rc_tut_btn
        #                 mask_button = bg_mask.find_element(By.XPATH, './/div[@class="mask_button rc_tut_btn"]')
        #                 print(111111111)
        #                 if mask_button:
        #                     # print('\n\n\n')
        #                     # print(index)
        #                     # print(mask_button)
        #                     # print('\n\n\n')
        #                     index += 1
        #                     action_chains.move_to_element(mask_button).perform()
        #                     driver.execute_script("arguments[0].click();", mask_button)
        #                 else:
        #                     # print('\n\n\n')
        #                     # print(1111111)
        #                     # print('\n\n\n')
        #                     flag = False
        #     except Exception as e:
        #         flag = False
        #         print("元素失效，请重新定位或等待一段时间后重试")
            

            # sleep(3600)

    @staticmethod
    def reptile_main_list(driver, account, password):
    # def reptile_main_list(self, driver, account, password, pool):
        LoginYY.login_yy(driver, account, password)
        if CONFIG.IM_REPTILE_FLAG == 'negative':
            # print(1)
            creator = produce()
            LoginYY.process_negative(driver, creator)
        elif CONFIG.IM_REPTILE_FLAG == 'positive':
            print(2)
            creator = produce()
            LoginYY.process_positive(driver, creator)
        elif CONFIG.IM_REPTILE_FLAG == 'detail':
            consumer(driver, LoginYY)
        sleep(3600)



    @staticmethod
    def process_negative(driver, produce):
    # def process_negative(self, driver):
        try:

            # 记录开始时间
            start_time = time.time()
            
            # sport_items.click()
            # 创建 ActionChains 对象
            action_chains = ActionChains(driver)
            
            # 等待 iframe 出现
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
            )
            
            # 获取 iframe 的 src 属性
            # iframe_src = iframe.get_attribute('src')
            # print(iframe_src)
            # param = iframe_src.split('?')[1]

            # 切换到 iframe
            driver.switch_to.frame(iframe)
            
            # 获取 iframe 内的 HTML
            # iframe_html = driver.page_source
            # print(iframe_html)
            
            try:
                
                game_element = WebDriverWait(driver, 10).until(
                    # EC.visibility_of_element_located((By.CLASS_NAME, 'leftmenu_sports_content'))
                    EC.visibility_of_element_located((By.XPATH, './/div[@class="leftmenu_sports_content default"]'))
                )

                # action_chains.move_to_element(game_element).perform()

                print(111000)
                # print(game_element)

                # leftmenu_sports_content_L1
                menu_items = game_element.find_elements(By.CLASS_NAME, 'leftmenu_sports_content_L1')
                for menu_item in menu_items:
                    # print('\n\n')
                    # print(menu_item.get_attribute('outerHTML'))

                    item_divs = menu_item.find_elements(By.XPATH, './/div')
                    for item_div in item_divs:
                        txt = item_div.get_attribute('innerHTML')
                        if txt == '波胆 / 反波胆':
                            action_chains.move_to_element(menu_item).perform()
                            driver.execute_script("arguments[0].click();", menu_item)
                            break
                        # break
            except Exception as e:
                print(e)


            # market_2_1
            game_content = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'market_3_1'))
            )

            # _info_soccer_correctscore
            game_event_row_cs = game_content.find_elements(By.XPATH, './/div[@class="row_live _info_soccer_correctscore"]')
            json_array = []

            detail_urls = []

            for event_row_item in game_event_row_cs:
                # print(event_row_item.get_attribute('outerHTML'))
                # json_data = {}
                event_row_cs = event_row_item.find_elements(By.XPATH, './/div[@class="event_row_cs"]')

                event_row_cs_item_1 = event_row_cs[0]
                event_row_cs_item_2 = event_row_cs[1]
                event_row_cs_item_3 = event_row_cs[2]
                event_row_cs_item_4 = event_row_cs[3]


                event_cs_mid_title = event_row_cs_item_1.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                title_items = event_cs_mid_title.find_elements(By.XPATH, './/div[@class="title_wrap"]')


                # 全场开始
                event_cs_mid_values_1 = event_row_cs_item_2.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                event_cs_mid_values_line_1_array = event_cs_mid_values_1.find_elements(By.XPATH, './/div[@class="event_row_inner_content"]')

                event_cs_mid_values_line_1_1 = event_cs_mid_values_line_1_array[0]
                event_cs_mid_values_line_1_2 = event_cs_mid_values_line_1_array[1]
                event_cs_mid_values_line_1_1_values = event_cs_mid_values_line_1_1.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_1_2_values = event_cs_mid_values_line_1_2.find_elements(By.XPATH, './/div[@class="odds_wrap"]')

                # event_cs_right
                event_cs_right_values_1 = event_row_cs_item_2.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                event_cs_right_values_1_line = event_cs_right_values_1.find_element(By.XPATH, './/div[@class="event_row_inner_content"]')
                event_cs_right_values_1_line_values = event_cs_right_values_1_line.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                # 全场结束
                
                #上半场开始
                event_cs_mid_values_2 = event_row_cs_item_3.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                event_cs_mid_values_line_2_array = event_cs_mid_values_2.find_elements(By.XPATH, './/div[@class="event_row_inner_content"]')

                event_cs_mid_values_line_2_1 = event_cs_mid_values_line_2_array[0]
                event_cs_mid_values_line_2_2 = event_cs_mid_values_line_2_array[1]
                event_cs_mid_values_line_2_1_values = event_cs_mid_values_line_2_1.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_2_2_values = event_cs_mid_values_line_2_2.find_elements(By.XPATH, './/div[@class="odds_wrap"]')

                # event_cs_right
                event_cs_right_values_2 = event_row_cs_item_3.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                event_cs_right_values_2_line = event_cs_right_values_2.find_element(By.XPATH, './/div[@class="event_row_inner_content"]')
                event_cs_right_values_2_line_values = event_cs_right_values_2_line.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                # 上半场结束


                #下半场开始
                event_cs_mid_values_3 = event_row_cs_item_4.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                event_cs_mid_values_line_3_array = event_cs_mid_values_3.find_elements(By.XPATH, './/div[@class="event_row_inner_content"]')

                event_cs_mid_values_line_3_1 = event_cs_mid_values_line_3_array[0]
                event_cs_mid_values_line_3_2 = event_cs_mid_values_line_3_array[1]
                event_cs_mid_values_line_3_1_values = event_cs_mid_values_line_3_1.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_3_2_values = event_cs_mid_values_line_3_2.find_elements(By.XPATH, './/div[@class="odds_wrap"]')

                # event_cs_right
                event_cs_right_values_3 = event_row_cs_item_4.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                event_cs_right_values_3_line = event_cs_right_values_3.find_element(By.XPATH, './/div[@class="event_row_inner_content"]')
                event_cs_right_values_3_line_values = event_cs_right_values_3_line.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                # 下半场结束

                up_json_data = {}
                down_json_data = {}
                all_json_data = {}
                for index, title_item in enumerate(title_items):
                    
                    # print('\n')
                    # print(title_item.get_attribute('outerHTML'))
                    # print('\n')
                    title = title_item.get_attribute('innerHTML')
                    # print(title)

                    # 全场开始
                    home_team_1_item = event_cs_mid_values_line_1_1_values[index]
                    away_team_1_item = event_cs_mid_values_line_1_2_values[index]
                    # print(home_team_item.get_attribute('outerHTML'))

                    home_team_1_value = ""
                    try:
                        home_team_1_item_span = home_team_1_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if home_team_1_item_span:
                            home_team_1_value = home_team_1_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        home_team_1_value = ""
                        # print(e)

                    away_team_1_value = ""
                    try:
                        away_team_1_item_span = away_team_1_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if away_team_1_item_span:
                            away_team_1_value = away_team_1_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        away_team_1_value = ""
                        # print(e)

                    all_json_data[title] = {
                        "home_team": home_team_1_value,
                        "away_team": away_team_1_value
                    }
                    # 全场结束

                    # 上半场场开始
                    home_team_2_item = event_cs_mid_values_line_2_1_values[index]
                    away_team_2_item = event_cs_mid_values_line_2_2_values[index]
                    # print(home_team_item.get_attribute('outerHTML'))

                    home_team_2_value = ""
                    try:
                        home_team_2_item_span = home_team_2_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if home_team_2_item_span:
                            home_team_2_value = home_team_2_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        home_team_2_value = ""
                        # print(e)

                    away_team_2_value = ""
                    try:
                        away_team_2_item_span = away_team_2_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if away_team_2_item_span:
                            away_team_2_value = away_team_2_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        away_team_2_value = ""
                        # print(e)

                    
                    up_json_data[title] = {
                        "home_team": home_team_2_value,
                        "away_team": away_team_2_value
                    }
                    # 上半场场开始

                    # 下半场开始
                    home_team_3_item = event_cs_mid_values_line_3_1_values[index]
                    away_team_3_item = event_cs_mid_values_line_3_2_values[index]
                    # print(home_team_item.get_attribute('outerHTML'))

                    home_team_3_value = ""
                    try:
                        home_team_3_item_span = home_team_3_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if home_team_3_item_span:
                            home_team_3_value = home_team_3_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        home_team_3_value = ""
                        # print(e)

                    away_team_3_value = ""
                    try:
                        away_team_3_item_span = away_team_3_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if away_team_3_item_span:
                            away_team_3_value = away_team_3_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        away_team_3_value = ""
                        # print(e)

                    
                    down_json_data[title] = {
                        "home_team": home_team_3_value,
                        "away_team": away_team_3_value
                    }
                    # 下半场结束


                event_cs_right_title = event_row_cs_item_1.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                title_items = event_cs_right_title.find_elements(By.XPATH, './/div[@class="title_wrap"]')

                for index, title_item in enumerate(title_items):
                    title = title_item.get_attribute('innerHTML')
                    
                    # 全场开始
                    value_1_item = event_cs_right_values_1_line_values[index]
                    value_1 = ""
                    try:
                        value_1_item_span = value_1_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if value_1_item_span:
                            value_1 = value_1_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        value_1 = ""

                    all_json_data[title] = value_1
                    # 全场结束

                    # 上半场开始
                    value_2_item = event_cs_right_values_2_line_values[index]
                    value_2 = ""
                    try:
                        value_2_item_span = value_2_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if value_2_item_span:
                            value_2 = value_2_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        value_2 = ""

                    up_json_data[title] = value_2
                    # 上半场开始

                    # 下半场开始
                    value_3_item = event_cs_right_values_3_line_values[index]
                    value_3 = ""
                    try:
                        value_3_item_span = value_3_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if value_3_item_span:
                            value_3 = value_3_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        value_3 = ""

                    down_json_data[title] = value_3
                    # 下半场开始

                # print(all_json_data)
                # print(up_json_data)
                # print(down_json_data)

                datetime_content = event_row_item.find_element(By.XPATH, './/div[@class="datetime"]')

                match_score_value = ''
                try:
                    match_score = datetime_content.find_element(By.XPATH, './/div[@class="score"]')
                    match_score_value = match_score.get_attribute('innerHTML')
                except Exception as e:
                    print("1元素失效，请重新定位或等待一段时间后重试")

                # event_row_item_data = event_row_item.find_element(By.XPATH, './/div[@class="team"]')
                a_team = event_row_item.find_element(By.XPATH, './/a[@style="cursor: pointer; flex-grow: 1;"]')
                # print(a_team)
                href_value = a_team.get_attribute("href")
                # print(href_value)

                detail_urls.append(href_value)

                # # 创建事件循环
                # loop = asyncio.get_event_loop()
                
                # # 添加任务到事件循环
                # task = asyncio.ensure_future(LoginYY.add_detail_tasks(pool, href_value))
                
                # # 启动事件循环并运行任务
                # loop.run_until_complete(task)
                # asyncio.run(LoginYY.add_detail_tasks(pool, href_value))
                # asyncio.create_task(LoginYY.add_detail_tasks(pool, href_value))
                # LoginYY.add_detail_tasks(pool, href_value)

                # pool.add_task(href_value)
                # pool.start_pool()
                

                # 使用正则表达式匹配数字值
                pattern = r'/(\d+)/'  # 匹配斜杠内的数字
                matches = re.findall(pattern, href_value)
                # print(matches)
                data_id = 0
                # 输出匹配到的结果
                if matches:
                    data_id = matches[1]
                    # print(f'数据id{data_id}')  # 取第一个匹配结果
                else:
                    print("未找到匹配的数字值")

                # print('\n\n\n\n')
                # print(123123)
                # print(datetime_content.get_attribute('outerHTML'))
                # print('\n\n\n\n')

                match_times_value = ''
                try:
                    match_times = datetime_content.find_element(By.XPATH, './/span')
                    match_times_value = match_times.get_attribute('innerHTML')
                except Exception as e:
                    print("元素失效，请重新定位或等待一段时间后重试")

                # teamname_title
                teamname_titles = event_row_item.find_elements(By.XPATH, './/div[@class="teamname_title"]')
                home_team = teamname_titles[0]
                away_team = teamname_titles[1]


                home_team_value = home_team.get_attribute('innerHTML')
                away_team_value = away_team.get_attribute('innerHTML')

                try:
                    home_team_value = BeautifulSoup(home_team_value, 'html.parser')
                    home_team_value = home_team_value.get_text()
                except Exception as e:
                    print(f"Error occurred while creating BeautifulSoup object: {e}")
                try:
                    away_team_value = BeautifulSoup(away_team_value, 'html.parser')
                    away_team_value = away_team_value.get_text()
                except Exception as e:
                    print(f"Error occurred while creating BeautifulSoup object: {e}")
                    
                if '\xa0' in home_team_value:
                    home_team_value = home_team_value.replace('\xa0', ' ')
                    
                if '\xa0' in away_team_value:
                    away_team_value = away_team_value.replace('\xa0', ' ')


                data = {
                    "id": data_id,
                    "match_times": match_times_value,
                    "match_score": match_score_value,
                    "home_team": home_team_value,
                    "away_team": away_team_value,
                    "full": all_json_data,
                    "first": up_json_data,
                    "second": down_json_data 
                }
                # print('\n\n\n')
                # print(data)
                json_array.append(data)

            # pool.start_pool()
            # print('\n\n\n')
            # print(json.dumps(json_array, ensure_ascii=False))

            # 记录结束时间
            end_time = time.time()

            # 计算执行时间
            execution_time = end_time - start_time
            print('\n')

            result = {
                "flag": "滚球中",
                "data": json_array
            }

            param = json.dumps(result, ensure_ascii=False)
            print(json.loads(param))

            timestamp_millis = int(time.time() * 1000)
            # print("Current timestamp (milliseconds):", timestamp_millis)

            # 写入日志
            logger.info(f'传递list参数：{timestamp_millis}-{json.loads(param)}')
            
            # 发送POST请求
            response = requests.post(CONFIG.POST_LIST_URL, json=json.loads(param))
            
            # 打印响应内容
            print(f'上传list结果：{response.text}')
            # 写入日志
            # logger.info(f'传递list参数：{timestamp_millis}-{json.loads(param)}')
            logger.info(f'上传list结果：{timestamp_millis}-{response.text}')

            # asyncio.run(LoginYY.add_detail_tasks(pool, detail_urls))
            LoginYY.add_detail_tasks(produce, detail_urls)

            print(f"代码执行时间为：{execution_time} 秒")
            # sleep(2)
            print('\n\n\n\n\n')
            # 退出 iframe
            driver.switch_to.default_content()
            LoginYY.process_negative(driver, produce)
            driver.refresh()
            
            # pass
        except Exception as e:
            print(e)
            # 退出 iframe
            driver.switch_to.default_content()
            LoginYY.process_negative(driver, produce)
            driver.refresh()

    def add_detail_tasks(produce, detail_urls):
        for href_value in detail_urls:
            print(f'地址：{href_value}')

            produce.push_msg(href_value)


            # pool.add_task(href_value)
            # pool.start_pool()
        # async with pool:  # 使用异步上下文管理器确保池在任务结束后关闭
        #     await pool.start_pool()


    @staticmethod
    def process_positive(driver, pool):
    # def process_positive(self, driver):
        try:
            # 记录开始时间
            start_time = time.time()
            
            # sport_items.click()
            # 创建 ActionChains 对象
            action_chains = ActionChains(driver)
            
            # print(112345)
            
            game_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'leftmenu_sports_content'))
            )

            # print(game_element)
            # print(game_element.get_attribute('outerHTML'))

            # leftmenu_sports_content_L1
            menu_items = game_element.find_elements(By.CLASS_NAME, 'leftmenu_sports_content_L1')
            for menu_item in menu_items:
                # print('\n\n')
                # print(menu_item.get_attribute('outerHTML'))

                item_divs = menu_item.find_elements(By.XPATH, './/div')
                for item_div in item_divs:
                    txt = item_div.get_attribute('innerHTML')
                    if txt == '让球 & 大/小':
                        action_chains.move_to_element(menu_item).perform()
                        driver.execute_script("arguments[0].click();", menu_item)
                        break

            # market_2_1
            game_content = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'col_3_1'))
            )
            print('\n\n\n')
            print(game_content.get_attribute('outerHTML'))

            # _info_soccer_correctscore
            game_event_row_cs = game_content.find_elements(By.XPATH, './/div[@class="lazyload-wrapper "]')
            json_array = []
            for event_row_item in game_event_row_cs:
                # print(event_row_item.get_attribute('outerHTML'))
                # json_data = {}
                event_row_cs = event_row_item.find_elements(By.XPATH, './/div[@class="event_row_cs"]')

                event_row_cs_item_1 = event_row_cs[0]
                event_row_cs_item_2 = event_row_cs[1]
                event_row_cs_item_3 = event_row_cs[2]
                event_row_cs_item_4 = event_row_cs[3]


                event_cs_mid_title = event_row_cs_item_1.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                title_items = event_cs_mid_title.find_elements(By.XPATH, './/div[@class="title_wrap"]')


                # 全场开始
                event_cs_mid_values_1 = event_row_cs_item_2.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                event_cs_mid_values_line_1_array = event_cs_mid_values_1.find_elements(By.XPATH, './/div[@class="event_row_inner_content"]')

                event_cs_mid_values_line_1_1 = event_cs_mid_values_line_1_array[0]
                event_cs_mid_values_line_1_2 = event_cs_mid_values_line_1_array[1]
                event_cs_mid_values_line_1_1_values = event_cs_mid_values_line_1_1.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_1_2_values = event_cs_mid_values_line_1_2.find_elements(By.XPATH, './/div[@class="odds_wrap"]')

                # event_cs_right
                event_cs_right_values_1 = event_row_cs_item_2.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                event_cs_right_values_1_line = event_cs_right_values_1.find_element(By.XPATH, './/div[@class="event_row_inner_content"]')
                event_cs_right_values_1_line_values = event_cs_right_values_1_line.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                # 全场结束
                
                #上半场开始
                event_cs_mid_values_2 = event_row_cs_item_3.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                event_cs_mid_values_line_2_array = event_cs_mid_values_2.find_elements(By.XPATH, './/div[@class="event_row_inner_content"]')

                event_cs_mid_values_line_2_1 = event_cs_mid_values_line_2_array[0]
                event_cs_mid_values_line_2_2 = event_cs_mid_values_line_2_array[1]
                event_cs_mid_values_line_2_1_values = event_cs_mid_values_line_2_1.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_2_2_values = event_cs_mid_values_line_2_2.find_elements(By.XPATH, './/div[@class="odds_wrap"]')

                # event_cs_right
                event_cs_right_values_2 = event_row_cs_item_3.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                event_cs_right_values_2_line = event_cs_right_values_2.find_element(By.XPATH, './/div[@class="event_row_inner_content"]')
                event_cs_right_values_2_line_values = event_cs_right_values_2_line.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                # 上半场结束


                #下半场开始
                event_cs_mid_values_3 = event_row_cs_item_4.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                event_cs_mid_values_line_3_array = event_cs_mid_values_3.find_elements(By.XPATH, './/div[@class="event_row_inner_content"]')

                event_cs_mid_values_line_3_1 = event_cs_mid_values_line_3_array[0]
                event_cs_mid_values_line_3_2 = event_cs_mid_values_line_3_array[1]
                event_cs_mid_values_line_3_1_values = event_cs_mid_values_line_3_1.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_3_2_values = event_cs_mid_values_line_3_2.find_elements(By.XPATH, './/div[@class="odds_wrap"]')

                # event_cs_right
                event_cs_right_values_3 = event_row_cs_item_4.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                event_cs_right_values_3_line = event_cs_right_values_3.find_element(By.XPATH, './/div[@class="event_row_inner_content"]')
                event_cs_right_values_3_line_values = event_cs_right_values_3_line.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                # 下半场结束

                up_json_data = {}
                down_json_data = {}
                all_json_data = {}
                for index, title_item in enumerate(title_items):
                    
                    # print('\n')
                    # print(title_item.get_attribute('outerHTML'))
                    # print('\n')
                    title = title_item.get_attribute('innerHTML')
                    # print(title)

                    # 全场开始
                    home_team_1_item = event_cs_mid_values_line_1_1_values[index]
                    away_team_1_item = event_cs_mid_values_line_1_2_values[index]
                    # print(home_team_item.get_attribute('outerHTML'))

                    home_team_1_value = ""
                    try:
                        home_team_1_item_span = home_team_1_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if home_team_1_item_span:
                            home_team_1_value = home_team_1_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        home_team_1_value = ""
                        # print(e)

                    away_team_1_value = ""
                    try:
                        away_team_1_item_span = away_team_1_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if away_team_1_item_span:
                            away_team_1_value = away_team_1_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        away_team_1_value = ""
                        # print(e)
                    
                    all_json_data[title] = {
                        "home_team": home_team_1_value,
                        "away_team": away_team_1_value
                    }
                    # 全场结束

                    # 上半场场开始
                    home_team_2_item = event_cs_mid_values_line_2_1_values[index]
                    away_team_2_item = event_cs_mid_values_line_2_2_values[index]
                    # print(home_team_item.get_attribute('outerHTML'))

                    home_team_2_value = ""
                    try:
                        home_team_2_item_span = home_team_2_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if home_team_2_item_span:
                            home_team_2_value = home_team_2_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        home_team_2_value = ""
                        # print(e)

                    away_team_2_value = ""
                    try:
                        away_team_2_item_span = away_team_2_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if away_team_2_item_span:
                            away_team_2_value = away_team_2_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        away_team_2_value = ""
                        # print(e)
                    
                    up_json_data[title] = {
                        "home_team": home_team_2_value,
                        "away_team": away_team_2_value
                    }
                    # 上半场场开始

                    # 下半场开始
                    home_team_3_item = event_cs_mid_values_line_3_1_values[index]
                    away_team_3_item = event_cs_mid_values_line_3_2_values[index]
                    # print(home_team_item.get_attribute('outerHTML'))

                    home_team_3_value = ""
                    try:
                        home_team_3_item_span = home_team_3_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if home_team_3_item_span:
                            home_team_3_value = home_team_3_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        home_team_3_value = ""
                        # print(e)

                    away_team_3_value = ""
                    try:
                        away_team_3_item_span = away_team_3_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if away_team_3_item_span:
                            away_team_3_value = away_team_3_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        away_team_3_value = ""
                        # print(e)
                    
                    down_json_data[title] = {
                        "home_team": home_team_3_value,
                        "away_team": away_team_3_value
                    }
                    # 下半场结束


                event_cs_right_title = event_row_cs_item_1.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                title_items = event_cs_right_title.find_elements(By.XPATH, './/div[@class="title_wrap"]')

                for index, title_item in enumerate(title_items):
                    title = title_item.get_attribute('innerHTML')
                    
                    # 全场开始
                    value_1_item = event_cs_right_values_1_line_values[index]
                    value_1 = ""
                    try:
                        value_1_item_span = value_1_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if value_1_item_span:
                            value_1 = value_1_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        value_1 = ""

                    all_json_data[title] = value_1
                    # 全场结束

                    # 上半场开始
                    value_2_item = event_cs_right_values_2_line_values[index]
                    value_2 = ""
                    try:
                        value_2_item_span = value_2_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if value_2_item_span:
                            value_2 = value_2_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        value_2 = ""

                    up_json_data[title] = value_2
                    # 上半场开始

                    # 下半场开始
                    value_3_item = event_cs_right_values_3_line_values[index]
                    value_3 = ""
                    try:
                        value_3_item_span = value_3_item.find_element(By.XPATH, './/span[@class="odds"]')
                        if value_3_item_span:
                            value_3 = value_3_item_span.get_attribute('innerHTML')
                    except Exception as e:
                        value_3 = ""

                    down_json_data[title] = value_3
                    # 下半场开始

                # print(all_json_data)
                # print(up_json_data)
                # print(down_json_data)

                print('\n\n\n\n')
                print(123123)
                print(event_row_item.get_attribute('outerHTML'))
                print('\n\n\n\n')

                datetime_content = event_row_item.find_element(By.XPATH, './/div[@class="datetime"]')

                

                # print('\n\n\n\n')
                # print(123123)
                # print(datetime_content.get_attribute('outerHTML'))
                # print('\n\n\n\n')
                match_score_value = ''
                try:
                    match_score = datetime_content.find_element(By.XPATH, './/div[@class="score"]')
                    match_score_value = match_score.get_attribute('innerHTML')
                except Exception as e:
                    print("元素失效，请重新定位或等待一段时间后重试")

                match_times_value = ''
                try:
                    match_times = datetime_content.find_element(By.XPATH, './/span')
                    match_times_value = match_times.get_attribute('innerHTML')
                except Exception as e:
                    print("元素失效，请重新定位或等待一段时间后重试")

                # teamname_title
                teamname_titles = event_row_item.find_elements(By.XPATH, './/div[@class="teamname_title"]')
                home_team = teamname_titles[0]
                away_team = teamname_titles[1]


                home_team_value = home_team.get_attribute('innerHTML')
                away_team_value = away_team.get_attribute('innerHTML')

                data = {
                    "match_times": match_times_value,
                    "match_score": match_score_value,
                    "home_team": home_team_value,
                    "away_team": away_team_value,
                    "full": all_json_data,
                    "first": up_json_data,
                    "second": down_json_data 
                }
                # print('\n\n\n')
                # print(data)
                json_array.append(data)

            print('\n\n\n')
            print(json_array)

            # 记录结束时间
            end_time = time.time()

            # 计算执行时间
            execution_time = end_time - start_time
            print('\n')

            print(f"代码执行时间为：{execution_time} 秒")
            # sleep(2)
            print('\n\n\n\n\n')
            # self.process_negative(driver)
            # driver.refresh()
            
            # pass
        except Exception as e:
            print(e)
            # self.process_negative(driver)
            # driver.refresh()



    def reptile_detail_data(driver, url):

        # 等待 iframe 出现
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
        )
            
        # 获取 iframe 的 src 属性
        iframe_src = iframe.get_attribute('src')
        print(iframe_src)
        param = iframe_src.split('?')[1]

        # return
        # driver.get(f'{url}&{param}')

        # 使用 JavaScript 设置 iframe 的 src 属性
        driver.execute_script(f"arguments[0].src = '{url}?{param}';", iframe)

        driver.switch_to.frame(iframe)

        game_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, './/div[@class="scr_wrp"]'))
        )
        print('\n\n\n')
        print(game_element)
        print('\n\n\n')
        data = {}

        pattern = r'/(\d+)/'  # 匹配斜杠内的数字
        matches = re.findall(pattern, url)
        print(matches)
        data_id = 0
        data['data_id'] = data_id
        # 输出匹配到的结果
        if matches:
            data['data_id'] = matches[1]

        src_header = game_element.find_element(By.XPATH, './/div[@class="scr_header"]')

        scr_title = src_header.find_element(By.XPATH, './/div[@class="scr_title"]')

        scr_title_span = scr_title.find_element(By.XPATH, './/span')

        scr_title_value = scr_title_span.get_attribute('innerHTML')

        data['title'] = scr_title_value

        scr_rows = game_element.find_elements(By.XPATH, './/div[@class="scr_row"]')

        if scr_rows:
            for i, row in enumerate(scr_rows):

                scr_title = row.find_element(By.XPATH, './/div[@class="scr_title"]')

                scr_title_value = scr_title.get_attribute('innerHTML')

                team = {}
                team['name'] = scr_title_value

                # print('\n\n\n')
                # print(scr_title_value)
                print('\n\n\n')
                
                scr_title_1_scr_details = row.find_element(By.XPATH, './/div[@class="scr_details"]')

                scr_title_1_scr_items = scr_title_1_scr_details.find_elements(By.XPATH, './/div')

                if scr_title_1_scr_items:
                    for index, item in enumerate(scr_title_1_scr_items):
                        if index == 0:
                            team['first'] = item.get_attribute('innerHTML')
                        if index == 1:
                            team['full'] = item.get_attribute('innerHTML')
                        if index == 2:
                            team['yellow'] = item.get_attribute('innerHTML')
                        if index == 3:
                            team['red'] = item.get_attribute('innerHTML')
                        if index == 4:
                            team['penalty'] = item.get_attribute('innerHTML')

                if i == 0:
                    data['home_team'] = team
                elif i == 1:
                    data['away_team'] = team
        
        # 退出 iframe，回到主文档
        driver.switch_to.default_content()

        print('\n\n\n')
        param = json.dumps(data, ensure_ascii=False)
        print(json.loads(param))

        # 发送POST请求
        response = requests.post(CONFIG.POST_DETAIL_URL, json=json.loads(param))

        # 打印响应内容
        print(f'上传detail结果：{response.text}')
        

        # pass