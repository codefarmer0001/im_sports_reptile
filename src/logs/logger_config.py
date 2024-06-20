import logging
import logging.handlers

def setup_logger(name='my_logger'):
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 创建 TimedRotatingFileHandler，文件按天轮换，保存7天的日志
    handler = logging.handlers.TimedRotatingFileHandler('log.log', when='midnight', interval=1, backupCount=7)
    handler.setLevel(logging.INFO)

    # 创建并设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # 将处理器添加到日志记录器
    if not logger.handlers:
        logger.addHandler(handler)

def getLogger(name='my_logger'):
    setup_logger(name)
    return logging.getLogger(name)