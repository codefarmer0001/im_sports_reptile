
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from config import CONFIG
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.common.exceptions import StaleElementReferenceException


class LoginYY:

    def __init__(self) -> None:
        pass

    

    def login_yy(self, driver):
        
        # 打开网页
        url = 'https://o3q.mltyz6.com/'

        driver.get(url)

        # try:
        if 1 == 1:
            element = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'buttons'))
            )
            # 登陆界面，打开登陆dialog
            # print(element)
            login_button = element.find_element(By.XPATH, '//button[@class="el-button el-button--primary login"]')
            # print(login_button.text)
            login_button.click()

            # pane-account
            login_panel = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, 'pane-account'))
            )
            # print(login_panel)
            input_user_name = login_panel.find_element(By.XPATH, '//input[@placeholder="请输入用户名"]')
            # print(input_user_name)
            input_user_name.send_keys('rmethan777')

            input_password = login_panel.find_element(By.XPATH, '//input[@placeholder="请输入密码"]')
            # print(input_password)
            input_password.send_keys('ethan7890')

            login_panal_submit = login_panel.find_element(By.XPATH, '//button[@type="submit"]')
            # print(login_panal_submit)
            login_panal_submit.click()

            # 主界面，登陆完后的界面

            main_panal_dialog = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'home-act-dialog'))
            )
            main_panal_dialog_close = main_panal_dialog.find_element(By.XPATH, '//button[@type="button" and @aria-label="Close"]')
            # print(main_panal_dialog_close)
            main_panal_dialog_close.click()


            # # navbar选项
            main_panal_navbar = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'navbar'))
            )
            sport_items = main_panal_navbar.find_element(By.XPATH, './/li[@class="sport"]')
            # print('\n\n\n')
            # print(sport_items.get_attribute('outerHTML'))

            sport_items_lable = sport_items.find_element(By.XPATH, './/span[@class="label"]')

            # sport_items.click()
            # 创建 ActionChains 对象
            action_chains = ActionChains(driver)

            # print('\n\n\n')
            # print(sport_items_lable.get_attribute('outerHTML'))
            # print('\n\n\n')

            # # 将鼠标移动到元素上
            action_chains.move_to_element(sport_items_lable).perform()


            sport_swiper = sport_items.find_element(By.XPATH, './/div[@class="swiper-wrapper"]')
            # print(sport_swiper.get_attribute('outerHTML'))

            sport_swiper_items = sport_swiper.find_elements(By.XPATH, './/div[@class="plat"]')
            # print(sport_swiper_items)
            if sport_swiper_items:
                for item in sport_swiper_items:
                    # print(item.get_attribute('outerHTML'))
                    item_span = item.find_element(By.XPATH, './/span')
                    # print(item_span.get_attribute('innerHTML'))
                    txt = item_span.get_attribute('innerHTML')
                    if txt == 'IM体育':
                        next = sport_items.find_element(By.XPATH, './/div[@aria-label="Next slide" and @aria-disabled="false"]')
                        # print(next.is_enabled())
                        action_chains.move_to_element(next).perform()
                        driver.execute_script("arguments[0].click();", next)

                        taget_item = item.find_element(By.XPATH, './/div[@class="main-pic"]')
                        action_chains.move_to_element(taget_item).perform()
                        driver.execute_script("arguments[0].click();", taget_item)
            
            # 切换到新标签页
            handles = driver.window_handles
            driver.switch_to.window(handles[1])  # 切换到第二个标签页（索引从0开始）
            self.process_login(driver)


            
        

            sleep(3600)
        # except Exception as e:
        #     print(e)


    def process_login(self, driver):

        # sport_items.click()
        # 创建 ActionChains 对象
        action_chains = ActionChains(driver)
        self.flag = True
        index = 0

        try:
            bg_mask = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'bg_mask'))
            )
            
            if bg_mask:
                while self.flag:
                # mask_button rc_tut_btn
                    mask_button = bg_mask.find_element(By.XPATH, './/div[@class="mask_button rc_tut_btn"]')
                    if mask_button:
                        print('\n\n\n')
                        print(index)
                        print(mask_button)
                        print('\n\n\n')
                        index += 1
                        action_chains.move_to_element(mask_button).perform()
                        driver.execute_script("arguments[0].click();", mask_button)
                    else:
                        print('\n\n\n')
                        print(1111111)
                        print('\n\n\n')
                        self.flag = False
        except StaleElementReferenceException:
            self.flag = False
            print("元素失效，请重新定位或等待一段时间后重试")
            # print(e)
                
        

        
        game_element = WebDriverWait(driver, 30).until(
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
                if txt == '波胆 / 反波胆':
                    action_chains.move_to_element(menu_item).perform()
                    driver.execute_script("arguments[0].click();", menu_item)
                    break
                # break

        # 
        # game_content = WebDriverWait(driver, 30).until(
        #     EC.visibility_of_element_located((By.ID, 'market_3_1'))
        # )
        # print('\n\n\n')
        # print(game_content.get_attribute('outerHTML'))

        # market_2_1
        game_content = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'market_3_1'))
        )
        # print('\n\n\n')
        # print(game_content.get_attribute('outerHTML'))

        # _info_soccer_correctscore
        game_event_row_cs = game_content.find_elements(By.XPATH, './/div[@class="row_live _info_soccer_correctscore"]')
        json_array = []
        for event_row_item in game_event_row_cs:
            # print(event_row_item.get_attribute('outerHTML'))
            # json_data = {}
            event_row_cs = event_row_item.find_elements(By.XPATH, './/div[@class="event_row_cs"]')

            event_row_cs_item_1 = event_row_cs[0]
            event_row_cs_item_2 = event_row_cs[1]
            event_row_cs_item_3 = event_row_cs[2]
            event_row_cs_item_4 = event_row_cs[3]

            # <div class="event_cs_mid">
            #     <div class="event_row_inner_header">
            #         <div class="title_wrap">1-0</div>
            #         <div class="title_wrap">2-0</div>
            #         <div class="title_wrap">2-1</div>
            #         <div class="title_wrap">3-0</div>
            #         <div class="title_wrap">3-1</div>
            #         <div class="title_wrap">3-2</div>
            #         <div class="title_wrap">4-0</div>
            #         <div class="title_wrap">4-1</div>
            #         <div class="title_wrap">4-2</div>
            #         <div class="title_wrap">4-3</div>
            #     </div>
            # </div>
            # <div class="event_cs_right">
            #     <div class="event_row_inner_header">
            #         <div class="title_wrap">0-0</div>
            #         <div class="title_wrap">1-1</div>
            #         <div class="title_wrap">2-2</div>
            #         <div class="title_wrap">3-3</div>
            #         <div class="title_wrap">4-4</div>
            #         <div class="title_wrap">其他</div>
            #     </div>
            # </div>
            event_cs_mid_title = event_row_cs_item_1.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
            title_items = event_cs_mid_title.find_elements(By.XPATH, './/div[@class="title_wrap"]')

            # <div class="event_cs_mid">
            #     <div class="event_row_inner_header">
            #         <div class="title_wrap">1-0</div>
            #         <div class="title_wrap">2-0</div>
            #         <div class="title_wrap">2-1</div>
            #         <div class="title_wrap">3-0</div>
            #         <div class="title_wrap">3-1</div>
            #         <div class="title_wrap">3-2</div>
            #         <div class="title_wrap">4-0</div>
            #         <div class="title_wrap">4-1</div>
            #         <div class="title_wrap">4-2</div>
            #         <div class="title_wrap">4-3</div>
            #     </div>
            # </div>
            # <div class="event_cs_right">
            #     <div class="event_row_inner_header">
            #         <div class="title_wrap">0-0</div>
            #         <div class="title_wrap">1-1</div>
            #         <div class="title_wrap">2-2</div>
            #         <div class="title_wrap">3-3</div>
            #         <div class="title_wrap">4-4</div>
            #         <div class="title_wrap">其他</div>
            #     </div>
            # </div>
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
            match_score = datetime_content.find_element(By.XPATH, './/div[@class="score"]')
            match_score_value = match_score.get_attribute('innerHTML')

            # print('\n\n\n\n')
            # print(datetime_content.get_attribute('outerHTML'))
            # print('\n\n\n\n')

            match_times = datetime_content.find_element(By.XPATH, './/span')
            match_times_value = match_times.get_attribute('innerHTML')

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

        # sleep(2)
        print('\n\n\n')
        self.process_login(driver)

            # title_items.append(right_title)
            # for title_item in title_items:
            #     print('\n')
            #     print(title_item.get_attribute('outerHTML'))
            #     print('\n')
            #     print(title_item.get_attribute('innerHTML'))


            # for index, event_row_cs_item in enumerate(event_row_cs):
            #     # print(index)
            #     # print(event_row_cs_item.get_attribute('outerHTML'))
            #     if index == 0:
            #         event_cs_mid_title = event_row_cs_item.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
            #         title_items = event_cs_mid_title.find_elements(By.XPATH, './/div[@class="title_wrap"]')
            #         for title_item in title_items:
            #             print('\n')
            #             print(title_item.get_attribute('innerHTML'))

            #         event_cs_right_title = event_row_cs_item.find_element(By.XPATH, './/div[@class="event_cs_right"]')
            #         title_items = event_cs_right_title.find_elements(By.XPATH, './/div[@class="title_wrap"]')
            #         for title_item in title_items:
            #             print('\n')
            #             print(title_item.get_attribute('innerHTML'))

            #         pass
            #     elif index == 1:
            #         pass
            #     elif index == 2:
            #         pass
            #     elif index == 3:
            #         pass

            # json_array.append(json_data)
        
                    

            

        driver.refresh()
        pass
