import redis
import time
from reptile.Detail import Detail

import os

mode = os.environ.get('MODE')

class consumer:

    def __init__(self, driver, loginYY) -> None:
        self.pool = redis.ConnectionPool(host='47.242.104.96', port=6379, db=0, password='Zaq123456..')
        self.redis_client = redis.StrictRedis(connection_pool=self.pool)
        self.consume_detail_tasks(driver)
        self.consume_list_tasks(driver)
        self.loginYY = loginYY
        # pass
        # 使用连接池连接到 Redis


    def process_task(self, driver, task):
        pass
        Detail.reptile_detail_data(driver, task.decode("utf-8"))

    # 模拟任务处理时间
    # time.sleep(1)

    def consume_detail_tasks(self, driver):
        while True:
            # 从队列中阻塞获取任务
            task = self.redis_client.brpop('task_queue', timeout=0)
            if task:
                self.process_task(driver, task[1])
            else:
                print('No tasks in the queue, waiting...')


    def consume_list_tasks(self, driver):
        while True:
            # 从队列中阻塞获取任务
            task = self.redis_client.brpop(mode, timeout=0)
            if task:
                self.process_task(driver, task[1])
            else:
                print('No tasks in the queue, waiting...')
