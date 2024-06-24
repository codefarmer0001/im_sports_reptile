import redis
from reptile.Detail import Detail
from reptile.MainData import MainData
from config import CONFIG
import os

mode = os.environ.get('MODE')

class consumer:

    def __init__(self, driver, produce) -> None:
        self.pool = redis.ConnectionPool(host='47.242.104.96', port=6379, db=0, password='Zaq123456..')
        self.redis_client = redis.StrictRedis(connection_pool=self.pool)
        self.produce = produce
        self.consume_detail_tasks(driver)
        self.consume_list_tasks(driver, produce)
        # pass
        # 使用连接池连接到 Redis


    def process_detail_task(self, driver, task):
        # pass
        Detail.reptile_detail_data(driver, task.decode("utf-8"))

    # 模拟任务处理时间
    # time.sleep(1)

    def consume_detail_tasks(self, driver):
        if CONFIG.IM_REPTILE_FLAG == 'detail':
            while True:
                # 从队列中阻塞获取任务
                task = self.redis_client.brpop('task_queue', timeout=0)
                if task:
                    self.process_detail_task(driver, task[1])
                else:
                    print('No tasks in the queue, waiting...')


    def consume_list_tasks(self, driver, produce):
        if CONFIG.IM_REPTILE_FLAG == 'negative' or CONFIG.IM_REPTILE_FLAG == 'positive':
            print(mode)
            while True:
                # 从队列中阻塞获取任务
                task = self.redis_client.brpop(mode, timeout=0)
                if task:
                    self.process_list_task(driver, task[1], produce)
                else:
                    print('No tasks in the queue, waiting...')

    def process_list_task(self, driver, task, produce):
        # pass
        task = task.decode("utf-8")
        if task == 'negative':
            MainData.process_negative(driver, produce)
        elif task == 'positive':
            MainData.process_positive(driver, self.produce)
