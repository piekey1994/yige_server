import aiomysql
from my_config import default_config
from aiomysql import Pool
from aiomysql.cursors import DictCursor

class AsyncDB(object):
    @classmethod
    async def init_sql(cls):
        cls.pool:Pool = await aiomysql.create_pool(
            host=default_config['mysql']['host'], 
            port=default_config['mysql']['port'],
            user=default_config['mysql']['user'], 
            password=default_config['mysql']['password'],
            db=default_config['mysql']['db'], 
            autocommit=False,
            cursorclass=DictCursor
        )