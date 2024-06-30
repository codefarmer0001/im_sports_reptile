
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from config import CONFIG
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import json
import time
import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os

from logs import getLogger  # 导入日志配置模块
logger = getLogger('list')

mode = os.environ.get('MODE', 'DEV')


class list:


    @staticmethod
    def process_negative(driver, produce, r):
    # def process_negative(self, driver):


        print(f'\n\n执行list的时间为：{datetime.now()}\n\n')

        try:

            # 记录开始时间
            start_time = time.time()

            driver.refresh()
            
            # sport_items.click()
            # 创建 ActionChains 对象
            action_chains = ActionChains(driver)
            
            # 等待 iframe 出现
            iframe = WebDriverWait(driver, 3, poll_frequency=0.1).until(
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
                
                game_element = WebDriverWait(driver, 3, poll_frequency=0.1).until(
                    EC.visibility_of_element_located((By.XPATH, './/div[@class="leftmenu_sports_content default"]'))
                )

                # action_chains.move_to_element(game_element).perform()

                print(111000)
                # print(game_element)

                # leftmenu_sports_content_L1
                # menu_items = game_element.find_elements(By.CLASS_NAME, 'leftmenu_sports_content_L1')
                menu_items = driver.execute_script("return arguments[0].querySelectorAll('.leftmenu_sports_content_L1');", game_element)

                for menu_item in menu_items:
                    txt = driver.execute_script("return arguments[0].innerHTML;", menu_item)
                    if '波胆 / 反波胆' in txt:
                        action_chains.move_to_element(menu_item).perform()
                        driver.execute_script("arguments[0].click();", menu_item)
                        break

                # for menu_item in menu_items:
                #     # print('\n\n')
                #     # print(menu_item.get_attribute('outerHTML'))

                #     item_divs = menu_item.find_elements(By.XPATH, './/div')
                #     for item_div in item_divs:
                #         txt = item_div.get_attribute('innerHTML')
                #         if txt == '波胆 / 反波胆':
                #             action_chains.move_to_element(menu_item).perform()
                #             driver.execute_script("arguments[0].click();", menu_item)
                #             break
                        # break
            except Exception as e:
                print(e)


            # market_2_1
            game_content = WebDriverWait(driver, 3, poll_frequency=0.1).until(
                EC.visibility_of_element_located((By.ID, 'market_3_1'))
            )

            # _info_soccer_correctscore
            # game_event_row_cs = game_content.find_elements(By.XPATH, './/div[@class="row_live _info_soccer_correctscore"]')

            game_event_row_cs = driver.execute_script("return arguments[0].querySelectorAll('.row_live._info_soccer_correctscore');", game_content)

            json_array = []

            detail_urls = []

            for event_row_item in game_event_row_cs:
                # print(event_row_item.get_attribute('outerHTML'))
                # json_data = {}
                # event_row_cs = event_row_item.find_elements(By.XPATH, './/div[@class="event_row_cs"]')
                event_row_cs = driver.execute_script("return arguments[0].querySelectorAll('.event_row_cs');", event_row_item)

                event_row_cs_item_1 = event_row_cs[0]
                event_row_cs_item_2 = event_row_cs[1]
                event_row_cs_item_3 = event_row_cs[2]
                event_row_cs_item_4 = event_row_cs[3]


                # event_cs_mid_title = event_row_cs_item_1.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                # event_cs_mid_title = driver.execute_script("return arguments[0].querySelector('.event_cs_mid');", event_row_cs_item_1)
                # title_items = event_cs_mid_title.find_elements(By.XPATH, './/div[@class="title_wrap"]')
                # title_items = driver.execute_script("return arguments[0].querySelector('.title_wrap');", event_cs_mid_title)

                titles = driver.execute_script("""
                    var event_cs_mid_title = arguments[0].querySelector('.event_cs_mid');
                    return Array.from(event_cs_mid_title.querySelectorAll('.title_wrap')).map(element => element.innerHTML);
                    """, event_row_cs_item_1)
                
                # print(title_items)


                # 全场开始
                # event_cs_mid_values_1 = event_row_cs_item_2.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                # event_cs_mid_values_1 = driver.execute_script("return arguments[0].querySelector('.event_cs_mid');", event_row_cs_item_2)
                # # event_cs_mid_values_line_1_array = event_cs_mid_values_1.find_elements(By.XPATH, './/div[@class="event_row_inner_content"]')
                # event_cs_mid_values_line_1_array = driver.execute_script("return arguments[0].querySelector('.event_row_inner_content');", event_cs_mid_values_1)

                event_cs_mid_values_line_1_array = driver.execute_script("""
                    var event_cs_mid = arguments[0].querySelector('.event_cs_mid');
                    return event_cs_mid.querySelectorAll('.event_row_inner_content');
                    """, event_row_cs_item_2)
                
                # print(event_cs_mid_values_line_1_array)

                event_cs_mid_values_line_1_1 = event_cs_mid_values_line_1_array[0]
                event_cs_mid_values_line_1_2 = event_cs_mid_values_line_1_array[1]
                # event_cs_mid_values_line_1_1_values = event_cs_mid_values_line_1_1.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_1_1_values = driver.execute_script("return arguments[0].querySelectorAll('.odds_wrap');", event_cs_mid_values_line_1_1)
                # event_cs_mid_values_line_1_2_values = event_cs_mid_values_line_1_2.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_1_2_values = driver.execute_script("return arguments[0].querySelectorAll('.odds_wrap');", event_cs_mid_values_line_1_2)

                # event_cs_right
                # event_cs_right_values_1 = event_row_cs_item_2.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                # event_cs_right_values_1 = driver.execute_script("return arguments[0].querySelector('.event_cs_right');", event_row_cs_item_2)
                # # event_cs_right_values_1_line = event_cs_right_values_1.find_element(By.XPATH, './/div[@class="event_row_inner_content"]')
                # event_cs_right_values_1_line = driver.execute_script("return arguments[0].querySelector('.event_row_inner_content');", event_cs_right_values_1)
                # # event_cs_right_values_1_line_values = event_cs_right_values_1_line.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                # event_cs_right_values_1_line_values = driver.execute_script("return arguments[0].querySelectorAll('.odds_wrap');", event_cs_right_values_1_line)

                event_cs_right_values_1_line_values = driver.execute_script("""
                    var event_cs_right = arguments[0].querySelector('.event_cs_right');
                    var event_row_inner_content = event_cs_right.querySelector('.event_row_inner_content');
                    var odds_wrap = event_row_inner_content.querySelectorAll('.odds_wrap');
                    return odds_wrap;
                    """, event_row_cs_item_2)
                # 全场结束
                
                #上半场开始
                # event_cs_mid_values_2 = event_row_cs_item_3.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                event_cs_mid_values_2 = driver.execute_script("return arguments[0].querySelector('.event_cs_mid');", event_row_cs_item_3)
                # event_cs_mid_values_line_2_array = event_cs_mid_values_2.find_elements(By.XPATH, './/div[@class="event_row_inner_content"]')
                event_cs_mid_values_line_2_array = driver.execute_script("return arguments[0].querySelectorAll('.event_row_inner_content');", event_cs_mid_values_2)


                event_cs_mid_values_line_2_1 = event_cs_mid_values_line_2_array[0]
                event_cs_mid_values_line_2_2 = event_cs_mid_values_line_2_array[1]
                # event_cs_mid_values_line_2_1_values = event_cs_mid_values_line_2_1.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_2_1_values = driver.execute_script("return arguments[0].querySelectorAll('.odds_wrap');", event_cs_mid_values_line_2_1)
                # event_cs_mid_values_line_2_2_values = event_cs_mid_values_line_2_2.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_2_2_values = driver.execute_script("return arguments[0].querySelectorAll('.odds_wrap');", event_cs_mid_values_line_2_2)

                # event_cs_right
                # event_cs_right_values_2 = event_row_cs_item_3.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                # event_cs_right_values_2 = driver.execute_script("return arguments[0].querySelector('.event_cs_right');", event_row_cs_item_3)
                # # event_cs_right_values_2_line = event_cs_right_values_2.find_element(By.XPATH, './/div[@class="event_row_inner_content"]')
                # event_cs_right_values_2_line = driver.execute_script("return arguments[0].querySelector('.event_row_inner_content');", event_cs_right_values_2)
                # # event_cs_right_values_2_line_values = event_cs_right_values_2_line.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                # event_cs_right_values_2_line_values = driver.execute_script("return arguments[0].querySelectorAll('.odds_wrap');", event_cs_right_values_2_line)

                event_cs_right_values_2_line_values = driver.execute_script("""
                    var event_cs_right = arguments[0].querySelector('.event_cs_right');
                    var event_row_inner_content = event_cs_right.querySelector('.event_row_inner_content');
                    var odds_wrap = event_row_inner_content.querySelectorAll('.odds_wrap');
                    return odds_wrap;
                    """, event_row_cs_item_3)
                # 上半场结束

                

                #下半场开始
                # event_cs_mid_values_3 = event_row_cs_item_4.find_element(By.XPATH, './/div[@class="event_cs_mid"]')
                event_cs_mid_values_3 = driver.execute_script("return arguments[0].querySelector('.event_cs_mid');", event_row_cs_item_4)
                # event_cs_mid_values_line_3_array = event_cs_mid_values_3.find_elements(By.XPATH, './/div[@class="event_row_inner_content"]')
                event_cs_mid_values_line_3_array = driver.execute_script("return arguments[0].querySelectorAll('.event_row_inner_content');", event_cs_mid_values_3)

                

                event_cs_mid_values_line_3_1 = event_cs_mid_values_line_3_array[0]
                event_cs_mid_values_line_3_2 = event_cs_mid_values_line_3_array[1]
                # event_cs_mid_values_line_3_1_values = event_cs_mid_values_line_3_1.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_3_1_values = driver.execute_script("return arguments[0].querySelectorAll('.odds_wrap');", event_cs_mid_values_line_3_1)
                # event_cs_mid_values_line_3_2_values = event_cs_mid_values_line_3_2.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                event_cs_mid_values_line_3_2_values = driver.execute_script("return arguments[0].querySelectorAll('.odds_wrap');", event_cs_mid_values_line_3_2)

                # event_cs_right
                # event_cs_right_values_3 = event_row_cs_item_4.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                # event_cs_right_values_3 = driver.execute_script("return arguments[0].querySelector('.event_cs_right');", event_row_cs_item_4)
                # # event_cs_right_values_3_line = event_cs_right_values_3.find_element(By.XPATH, './/div[@class="event_row_inner_content"]')
                # event_cs_right_values_3_line = driver.execute_script("return arguments[0].querySelector('.event_row_inner_content');", event_cs_right_values_3)
                # # event_cs_right_values_3_line_values = event_cs_right_values_3_line.find_elements(By.XPATH, './/div[@class="odds_wrap"]')
                # event_cs_right_values_3_line_values = driver.execute_script("return arguments[0].querySelectorAll('.odds_wrap');", event_cs_right_values_3_line)

                event_cs_right_values_3_line_values = driver.execute_script("""
                    var event_cs_right = arguments[0].querySelector('.event_cs_right');
                    var event_row_inner_content = event_cs_right.querySelector('.event_row_inner_content');
                    var odds_wrap = event_row_inner_content.querySelectorAll('.odds_wrap');
                    return odds_wrap;
                    """, event_row_cs_item_4)
                # 下半场结束

                up_json_data = {}
                down_json_data = {}
                all_json_data = {}
                for index, title in enumerate(titles):
                    
                    # print('\n')
                    # print(title_item.get_attribute('outerHTML'))
                    # print('\n')
                    # title = title_item.get_attribute('innerHTML')
                    # print(title)
                    
                    # 全场开始
                    home_team_1_item = event_cs_mid_values_line_1_1_values[index]
                    away_team_1_item = event_cs_mid_values_line_1_2_values[index]
                    # print(home_team_item.get_attribute('outerHTML'))

                    home_team_1_value = driver.execute_script("""
                        var odds = arguments[0].querySelector('.odds');
                        if (odds) return odds.innerHTML;
                        return '';
                        """, home_team_1_item)
                    
                    # print(home_team_1_value)
                    # try:
                    #     # home_team_1_item_span = home_team_1_item.find_element(By.XPATH, './/span[@class="odds"]')
                    #     home_team_1_item_span = driver.execute_script("return arguments[0].querySelector('.odds').innerHTML;", home_team_1_item)
                    #     if home_team_1_item_span:
                    #         home_team_1_value = home_team_1_item_span.get_attribute('innerHTML')
                    # except Exception as e:
                    #     home_team_1_value = ""
                        # print(e)

                    away_team_1_value = driver.execute_script("""
                        var odds = arguments[0].querySelector('.odds');
                        if(odds) return odds.innerHTML;
                        return "";
                        """, away_team_1_item)
                    # try:
                    #     # away_team_1_item_span = away_team_1_item.find_element(By.XPATH, './/span[@class="odds"]')
                    #     away_team_1_item_span = driver.execute_script("""
                    #         return arguments[0].querySelector('.odds').innerHTML;
                    #         """, away_team_1_item)
                    #     if away_team_1_item_span:
                    #         away_team_1_value = away_team_1_item_span.get_attribute('innerHTML')
                    # except Exception as e:
                    #     away_team_1_value = ""
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

                    home_team_2_value = driver.execute_script("""
                        var odds = arguments[0].querySelector('.odds');
                        if(odds) return odds.innerHTML;
                        return "";
                        """, home_team_2_item)
                    # try:
                    #     # home_team_2_item_span = home_team_2_item.find_element(By.XPATH, './/span[@class="odds"]')
                    #     home_team_2_item_span = driver.execute_script("return arguments[0].querySelector('.odds');", home_team_2_item)
                    #     if home_team_2_item_span:
                    #         home_team_2_value = home_team_2_item_span.get_attribute('innerHTML')
                    # except Exception as e:
                    #     home_team_2_value = ""
                        # print(e)

                    away_team_2_value = driver.execute_script("""
                            var odds = arguments[0].querySelector('.odds');
                            if(odds) return odds.innerHTML;
                            return "";
                        """, away_team_2_item)
                    # try:
                    #     # away_team_2_item_span = away_team_2_item.find_element(By.XPATH, './/span[@class="odds"]')
                    #     away_team_2_item_span = driver.execute_script("return arguments[0].querySelector('.odds');", away_team_2_item)
                    #     if away_team_2_item_span:
                    #         away_team_2_value = away_team_2_item_span.get_attribute('innerHTML')
                    # except Exception as e:
                    #     away_team_2_value = ""
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

                    home_team_3_value = driver.execute_script("""
                        var odds = arguments[0].querySelector('.odds');
                        if(odds) return odds.innerHTML;
                        return "";
                        """, home_team_3_item)
                    # try:
                    #     # home_team_3_item_span = home_team_3_item.find_element(By.XPATH, './/span[@class="odds"]')
                    #     home_team_3_item_span = driver.execute_script("return arguments[0].querySelector('.odds');", home_team_3_item)
                    #     if home_team_3_item_span:
                    #         home_team_3_value = home_team_3_item_span.get_attribute('innerHTML')
                    # except Exception as e:
                    #     home_team_3_value = ""
                        # print(e)

                    away_team_3_value = driver.execute_script("""
                        var odds = arguments[0].querySelector('.odds');
                        if(odds) return odds.innerHTML;
                        return "";
                        """, away_team_3_item)
                    # try:
                    #     # away_team_3_item_span = away_team_3_item.find_element(By.XPATH, './/span[@class="odds"]')
                    #     away_team_3_item_span = driver.execute_script("return arguments[0].querySelector('.odds');", away_team_3_item)
                    #     if away_team_3_item_span:
                    #         away_team_3_value = away_team_3_item_span.get_attribute('innerHTML')
                    # except Exception as e:
                    #     away_team_3_value = ""
                        # print(e)

                    
                    down_json_data[title] = {
                        "home_team": home_team_3_value,
                        "away_team": away_team_3_value
                    }
                    # 下半场结束

                

                # event_cs_right_title = event_row_cs_item_1.find_element(By.XPATH, './/div[@class="event_cs_right"]')
                event_cs_right_title = driver.execute_script("return arguments[0].querySelector('.event_cs_right');", event_row_cs_item_1)
                # title_items = event_cs_right_title.find_elements(By.XPATH, './/div[@class="title_wrap"]')
                # title_items = driver.execute_script("return arguments[0].querySelectorAll('.title_wrap');", event_cs_right_title)

                titles = driver.execute_script(
                    """
                    var event_cs_right_title = arguments[0].querySelector('.event_cs_right');
                    var title_items = event_cs_right_title.querySelectorAll('.title_wrap');
                    var titles = [];
                    title_items.forEach(function(item) {
                        titles.push(item.innerText);
                    });
                    return titles;
                    """,
                    event_row_cs_item_1
                )
                
                for index, title in enumerate(titles):
                    # title = title_item.get_attribute('innerHTML')

                    # 全场开始
                    value_1_item = event_cs_right_values_1_line_values[index]
                    value_1 = driver.execute_script("""
                        var odds = arguments[0].querySelector('.odds');
                        if(odds) return odds.innerHTML;
                        return "";
                        """, value_1_item)
                    # try:
                    #     # value_1_item_span = value_1_item.find_element(By.XPATH, './/span[@class="odds"]')
                    #     value_1_item_span = driver.execute_script("return arguments[0].querySelector('.odds');", value_1_item)
                    #     if value_1_item_span:
                    #         value_1 = value_1_item_span.get_attribute('innerHTML')
                    # except Exception as e:
                    #     value_1 = ""

                    all_json_data[title] = value_1
                    # 全场结束

                    # 上半场开始
                    value_2_item = event_cs_right_values_2_line_values[index]
                    value_2 = driver.execute_script("""
                        var odds = arguments[0].querySelector('.odds');
                        if(odds) return odds.innerHTML;
                        return "";
                        """, value_2_item)
                    # try:
                    #     # value_2_item_span = value_2_item.find_element(By.XPATH, './/span[@class="odds"]')
                    #     value_2_item_span = driver.execute_script("return arguments[0].querySelector('.odds');", value_2_item)
                    #     if value_2_item_span:
                    #         value_2 = value_2_item_span.get_attribute('innerHTML')
                    # except Exception as e:
                    #     value_2 = ""

                    up_json_data[title] = value_2
                    # 上半场开始

                    # 下半场开始
                    value_3_item = event_cs_right_values_3_line_values[index]
                    value_3 = driver.execute_script("""
                        var odds = arguments[0].querySelector('.odds');
                        if(odds) return odds.innerHTML;
                        return "";
                        """, value_3_item)
                    # try:
                    #     # value_3_item_span = value_3_item.find_element(By.XPATH, './/span[@class="odds"]')
                    #     value_3_item_span = driver.execute_script("return arguments[0].querySelector('.odds');", value_3_item)
                    #     if value_3_item_span:
                    #         value_3 = value_3_item_span.get_attribute('innerHTML')
                    # except Exception as e:
                    #     value_3 = ""

                    down_json_data[title] = value_3
                    # 下半场开始

                # print(123123123)
                
                # print(all_json_data)
                # print(up_json_data)
                # print(down_json_data)

                # datetime_content = event_row_item.find_element(By.XPATH, './/div[@class="datetime"]')
                datetime_content = driver.execute_script("return arguments[0].querySelector('.datetime');", event_row_item)

                match_score_value = driver.execute_script("""
                        var score = arguments[0].querySelector('.score');
                        if(score) return score.innerHTML;
                        return "";
                        """, datetime_content)
                # try:
                #     # match_score = datetime_content.find_element(By.XPATH, './/div[@class="score"]')
                #     match_score = driver.execute_script("return arguments[0].querySelector('.score');", datetime_content)
                #     match_score_value = match_score.get_attribute('innerHTML')
                # except Exception as e:
                #     print("1元素失效，请重新定位或等待一段时间后重试")

                # event_row_item_data = event_row_item.find_element(By.XPATH, './/div[@class="team"]')
                a_team = event_row_item.find_element(By.XPATH, './/a[@style="cursor: pointer; flex-grow: 1;"]')
                # print(a_team)
                href_value = a_team.get_attribute("href")
                # print(href_value)

                detail_urls.append(href_value)
                

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

                match_times_value = ''
                try:
                    match_times = datetime_content.find_element(By.XPATH, './/span')
                    match_times_value = match_times.get_attribute('innerHTML')
                except Exception as e:
                    print("元素失效，请重新定位或等待一段时间后重试")

                # teamname_title
                # teamname_titles = event_row_item.find_elements(By.XPATH, './/div[@class="teamname_title"]')
                teamname_titles = driver.execute_script("return arguments[0].querySelectorAll('.teamname_title');", event_row_item)
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


            # print(2222222)

            # 记录结束时间
            end_time = time.time()

            # 计算执行时间
            execution_time = end_time - start_time
            print('\n')

            result = {
                "flag": "滚球中",
                "data": json_array
            }

            # print()

            param = json.dumps(result, ensure_ascii=False)
            print(json.loads(param))

            timestamp_millis = int(time.time() * 1000)
            # print("Current timestamp (milliseconds):", timestamp_millis)

            # 写入日志
            logger.info(f'传递list参数：{timestamp_millis}-{json.loads(param)}')

            driver.switch_to.default_content()
            produce.push_list(CONFIG.IM_REPTILE_FLAG)

            print(f"list解析结果总耗时：{time.time() - start_time} 秒")

            submit_start_time = time.time()

            # 发送POST请求
            response = requests.post(CONFIG.POST_LIST_URL, json=json.loads(param))
            
            # 打印响应内容
            print(f'上传list结果：{response.text}')
            # 写入日志
            # logger.info(f'传递list参数：{timestamp_millis}-{json.loads(param)}')
            logger.info(f'上传list结果：{timestamp_millis}-{response.text}')

            # asyncio.run(LoginYY.add_detail_tasks(pool, detail_urls))
            list.add_detail_tasks(produce, detail_urls)

            print(f"list 解析+上传{len(detail_urls)}条结果总耗时：{time.time() - start_time} 秒, 上传总耗时：{time.time() - submit_start_time} 秒")
            # sleep(2)
            print('\n\n\n\n\n')
            # 退出 iframe
            driver.switch_to.default_content()
            # LoginYY.process_negative(driver, produce, process_index + 1)
            # driver.refresh()


            last_login_time_str = r.get_string(mode)
            last_login_time = float(last_login_time_str)
            login_time = time.time() - last_login_time
            
            if login_time > 36000:
            # if login_time > 120:
                from .login import login
                print(f'登录时长：{login_time}')
                driver.quit()
                login.main()

            
            # pass
        except Exception as e:
            print(e)
            # 退出 iframe
            driver.switch_to.default_content()
            produce.push_list(CONFIG.IM_REPTILE_FLAG)
            # driver.switch_to.default_content()
            # LoginYY.process_negative(driver, produce, process_index + 1)
            # driver.refresh()

    def add_detail_tasks(produce, detail_urls):
        for href_value in detail_urls:
            print(f'地址：{href_value}')

            produce.push_detail(href_value)


    @staticmethod
    def process_positive(driver, pool, r):
    # def process_positive(self, driver):
        try:
            # 记录开始时间
            start_time = time.time()
            
            # sport_items.click()
            # 创建 ActionChains 对象
            action_chains = ActionChains(driver)
            
            # print(112345)
            
            game_element = WebDriverWait(driver, 3, poll_frequency=0.1).until(
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
            game_content = WebDriverWait(driver, 3, poll_frequency=0.1).until(
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

                print('\n\n\n\n')
                print(123123)
                print(event_row_item.get_attribute('outerHTML'))
                print('\n\n\n\n')

                datetime_content = event_row_item.find_element(By.XPATH, './/div[@class="datetime"]')

                
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

            # pass
        except Exception as e:
            print(e)

