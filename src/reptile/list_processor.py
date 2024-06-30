from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import re
import requests
from datetime import datetime
import os

from logs import getLogger  # 导入日志配置模块
logger = getLogger('list')

mode = os.environ.get('MODE', 'DEV')

class ListProcessor:

    @staticmethod
    def process_negative(driver, produce, r):
        print(f'\n\n执行list的时间为：{datetime.now()}\n\n')
        try:
            start_time = time.time()
            driver.refresh()
            
            action_chains = ActionChains(driver)
            iframe = WebDriverWait(driver, 3, poll_frequency=0.1).until(
                EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
            )
            driver.switch_to.frame(iframe)
            
            try:
                game_element = WebDriverWait(driver, 3, poll_frequency=0.1).until(
                    EC.visibility_of_element_located((By.XPATH, './/div[@class="leftmenu_sports_content default"]'))
                )
                menu_items = driver.execute_script("return arguments[0].querySelectorAll('.leftmenu_sports_content_L1');", game_element)
                for menu_item in menu_items:
                    txt = driver.execute_script("return arguments[0].innerHTML;", menu_item)
                    if '波胆 / 反波胆' in txt:
                        action_chains.move_to_element(menu_item).perform()
                        driver.execute_script("arguments[0].click();", menu_item)
                        break
            except Exception as e:
                print(e)

            game_content = WebDriverWait(driver, 3, poll_frequency=0.1).until(
                EC.visibility_of_element_located((By.ID, 'market_3_1'))
            )

            game_event_row_cs = driver.execute_script("return arguments[0].querySelectorAll('.row_live._info_soccer_correctscore');", game_content)
            json_array = []
            detail_urls = []

            for event_row_item in game_event_row_cs:
                all_json_data, up_json_data, down_json_data = {}, {}, {}
                event_row_cs = driver.execute_script("return arguments[0].querySelectorAll('.event_row_cs');", event_row_item)

                for idx, event_row_cs_item in enumerate(event_row_cs):
                    event_cs_mid_values = driver.execute_script("return arguments[0].querySelector('.event_cs_mid');", event_row_cs_item)
                    event_cs_mid_values_lines = driver.execute_script("return arguments[0].querySelectorAll('.event_row_inner_content');", event_cs_mid_values)

                    for line_idx, line in enumerate(event_cs_mid_values_lines):
                        odds_values = driver.execute_script("return arguments[0].querySelectorAll('.odds_wrap .odds');", line)
                        odds_texts = [driver.execute_script("return arguments[0].innerText;", odds) for odds in odds_values]

                        if idx == 0:
                            all_json_data[f"line_{line_idx}"] = odds_texts
                        elif idx == 1:
                            up_json_data[f"line_{line_idx}"] = odds_texts
                        else:
                            down_json_data[f"line_{line_idx}"] = odds_texts

                # 获取标题
                event_cs_mid_title = driver.execute_script("return arguments[0].querySelector('.event_cs_mid_title');", event_row_item)
                title_items = driver.execute_script("return arguments[0].querySelectorAll('.title_wrap');", event_cs_mid_title)

                for idx, title_item in enumerate(title_items):
                    title = f"title_{idx}"
                    all_json_data[title] = driver.execute_script("return arguments[0].innerText;", title_item)

                datetime_content = driver.execute_script("return arguments[0].querySelector('.datetime');", event_row_item)
                match_score_value = ""
                try:
                    match_score = driver.execute_script("return arguments[0].querySelector('.score');", datetime_content)
                    match_score_value = driver.execute_script("return arguments[0].innerHTML;", match_score)
                except:
                    pass

                a_team = driver.execute_script("return arguments[0].querySelector('a[style=\"cursor: pointer; flex-grow: 1;\"]');", event_row_item)
                href_value = driver.execute_script("return arguments[0].href;", a_team)
                detail_urls.append(href_value)

                pattern = r'/(\d+)/'
                matches = re.findall(pattern, href_value)
                data_id = matches[1] if matches else 0

                match_times_value = ""
                try:
                    match_times = driver.execute_script("return arguments[0].querySelector('.datetime span');", event_row_item)
                    match_times_value = driver.execute_script("return arguments[0].innerHTML;", match_times)
                except:
                    pass

                teamname_titles = driver.execute_script("return arguments[0].querySelectorAll('.teamname_title');", event_row_item)
                home_team_value = driver.execute_script("return arguments[0].innerHTML;", teamname_titles[0])
                away_team_value = driver.execute_script("return arguments[0].innerHTML;", teamname_titles[1])

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
                json_array.append(data)

            end_time = time.time()
            execution_time = end_time - start_time
            print('\n')

            result = {
                "flag": "滚球中",
                "data": json_array
            }

            param = json.dumps(result, ensure_ascii=False)
            print(json.loads(param))

            timestamp_millis = int(time.time() * 1000)
            logger.info(f'传递list参数：{timestamp_millis}-{json.loads(param)}')

            driver.switch_to.default_content()
            produce.push_list(CONFIG.IM_REPTILE_FLAG)

            print(f"list解析结果总耗时：{execution_time} 秒")

            submit_start_time = time.time()
            response = requests.post(CONFIG.POST_LIST_URL, json=json.loads(param))
            print(f'上传list结果：{response.text}')
            logger.info(f'上传list结果：{timestamp_millis}-{response.text}')

            ListProcessor.add_detail_tasks(produce, detail_urls)

            total_time = time.time() - start_time
            upload_time = time.time() - submit_start_time
            print(f"list 解析+上传{len(detail_urls)}条结果总耗时：{total_time} 秒, 上传总耗时：{upload_time} 秒")

            print('\n\n\n\n\n')
            driver.switch_to.default_content()

            last_login_time_str = r.get_string(mode)
            last_login_time = float(last_login_time_str)
            login_time = time.time() - last_login_time

            if login_time > 36000:
                from .login import login
                print(f'登录时长：{login_time}')
                driver.quit()
                login.main()

        except Exception as e:
            print(e)
            driver.switch_to.default_content()
            produce.push_list(CONFIG.IM_REPTILE_FLAG)

    @staticmethod
    def add_detail_tasks(produce, detail_urls):
        for url in detail_urls:
            produce.push_list_detail(url)