
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from config import CONFIG
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import json
import re
import requests
import time

from logs import getLogger  # 导入日志配置模块
logger = getLogger('detail')


# from pool import DriverPool

class Detail:

    @staticmethod
    def reptile_detail_data(driver, url):

        # 等待 iframe 出现
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
        )
            
        # 获取 iframe 的 src 属性
        iframe_src = iframe.get_attribute('src')
        # print(iframe_src)
        param = iframe_src.split('?')[1]
        print(url)
        print(param)
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

        scr_title_value = ''
        try:
            scr_title_span = scr_title.find_element(By.XPATH, './/span')
            scr_title_value = scr_title_span.get_attribute('innerHTML')
        except Exception as e:
            # print(e)
            scr_title_value = scr_title.get_attribute('innerHTML')


        # scr_title_span = scr_title.find_element(By.XPATH, './/span')

        # scr_title_value = scr_title_span.get_attribute('innerHTML')
        

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

        timestamp_millis = int(time.time() * 1000)
        # print("Current timestamp (milliseconds):", timestamp_millis)

        # 写入日志
        logger.info(f'上传detail参数：{timestamp_millis}-{json.loads(param)}')
        # 发送POST请求
        response = requests.post(CONFIG.POST_DETAIL_URL, json=json.loads(param))

        # 打印响应内容
        print(f'上传detail结果：{response.text}')

        # 写入日志
        # logger.info(f'上传detail参数：{timestamp_millis}-{json.loads(param)}')
        logger.info(f'上传detail结果：{timestamp_millis}-{response.text}')
        

        # pass