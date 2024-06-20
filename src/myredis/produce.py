import redis
from time import sleep

class produce:

    def __init__(self) -> None:
        # 连接到 Redis
        self.redis_client = redis.StrictRedis(host='47.242.104.96', port=6379, db=0, password='Zaq123456..')
        pass


    def push_msg(self, msg):
        # 向队列中添加任务
        # for i in range(1000):
        self.redis_client.lpush('task_queue', f'{msg}')
            # print(f'Added task_{i} to the queue')
            # sleep(1)

