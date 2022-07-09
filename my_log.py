import logging
from my_config import default_config

log_level={
    'debug':logging.DEBUG,
    'info':logging.INFO,
    'warn':logging.WARN,
    'error':logging.ERROR
}

logger = logging.getLogger('wenet')
logger.setLevel(logging.DEBUG)
# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(log_level[default_config['log']['level']])

# 定义handler的输出格式
formatter = logging.Formatter(
    '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
ch.close()

def format_log(id,text):
    return '[{}]{}'.format(id,text)