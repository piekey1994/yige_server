from uvicorn.workers import UvicornWorker
from my_config import default_config
class MyUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "loop":"uvloop",
        "http":"httptools",
        "access_log": default_config['server']['access_log']
    }