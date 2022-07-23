from fastapi import APIRouter
from my_config import default_config
import aiohttp
import json
from my_log import logger

router = APIRouter()

@router.get('/weapp/login/getopenid')
async def getopenid(code:str):
    appid = default_config['login']['appid']
    appsecret = default_config['login']['appsecret']
    curl = 'https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(
        appid,
        appsecret,
        code
    )
    async with aiohttp.request('get',curl) as response:
        res_json =json.loads(await response.text())
        logger.info(res_json)
        return {
            'status':1,
            'info':res_json
        }
