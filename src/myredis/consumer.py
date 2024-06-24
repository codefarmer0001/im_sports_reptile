import redis
from reptile.detail import detail
from reptile.list import list
from config import CONFIG
import os

mode = os.environ.get('MODE')

class consumer:

    def __init__(self, driver, produce, r) -> None:
        self.pool = redis.ConnectionPool(host=CONFIG.REDIS_HOST, port=CONFIG.REDIS_PORT, db=CONFIG.REDIS_DB, password=CONFIG.REDIS_PASSWORD)
        self.redis_client = redis.StrictRedis(connection_pool=self.pool)
        self.consume_detail_tasks(driver, r)
        self.consume_list_tasks(driver, produce, r)
        # pass
        # 使用连接池连接到 Redis


    def process_detail_task(self, driver, task, r):
        # pass
        detail.reptile_detail_data(driver, task.decode("utf-8"), r)

    # 模拟任务处理时间
    # time.sleep(1)

    def consume_detail_tasks(self, driver, r):
        if CONFIG.IM_REPTILE_FLAG == 'detail':
            while True:
                # 从队列中阻塞获取任务
                task = self.redis_client.brpop('task_queue', timeout=0)
                if task:
                    self.process_detail_task(driver, task[1], r)
                else:
                    print('No tasks in the queue, waiting...')


    def consume_list_tasks(self, driver, produce, r):
        if CONFIG.IM_REPTILE_FLAG == 'negative' or CONFIG.IM_REPTILE_FLAG == 'positive':
            print(mode)
            while True:
                # 从队列中阻塞获取任务
                task = self.redis_client.brpop(mode, timeout=0)
                if task:
                    self.process_list_task(driver, task[1], produce, r)
                else:
                    print('No tasks in the queue, waiting...')

    def process_list_task(self, driver, task, produce, r):
        # pass
        task = task.decode("utf-8")
        if task == 'negative':
            list.process_negative(driver, produce, r)
        elif task == 'positive':
            list.process_positive(driver, produce, r)
