from my_config import default_config

bind='0.0.0.0:{}'.format(default_config['server']['port'])
workers = default_config['server']['num']
worker_class = 'uvicorn_app.MyUvicornWorker'
timeout = 0 #关闭主进程超时重启机制