from my_log import logger
from fastapi import APIRouter,Form
from my_config import default_config
from db.analyze_model import AnalyzeModel
from urllib.parse import urlencode
import aiohttp
import time
import base64
import hashlib
import hmac

router = APIRouter()

def get_hamc_sha1(message, key):
    message = message.encode()  # 加密内容
    key = key.encode()          # 加密的key
    result = hmac.new(key, message, hashlib.sha1).digest()  # 返回结果：b'\xd5*\x01\xb0\xa4,y\x96\x9d`\xd7\xfcB\xe1\x95OZIe\xe7'
    _sig = base64.b64encode(result).decode()
    return _sig


@router.post('/weapp/analyze/getTypeData')
async def getTypeData(openid:str=Form()):
    type_data = await AnalyzeModel.getTypeData(openid)
    return {
        'code':1,
        'data':type_data
    }

@router.post('/weapp/analyze/getWeather')
async def getWeather(latitude:float=Form(),longitude:float=Form()):
    param={
        'location':'{},{}'.format(latitude,longitude),
        'key':default_config['weather']['city_key']
    }
    url = '{}?{}'.format(default_config['weather']['city_url'],urlencode(param))
    async with aiohttp.request('get',url) as response:
        city_res = await response.json()
    location=city_res['result']['ad_info']['city']
    key = default_config['weather']['xz_key']
    uid = default_config['weather']['xz_uid']
    api = default_config['weather']['xz_api']
    param={
        'ts':int(time.time()),
        'ttl':300,
        'uid':uid
    }
    sig_data = urlencode(param)
    sig = get_hamc_sha1(sig_data,key)
    param['sig'] = sig # 签名
    param['location'] = location
    param['start'] = 0 # 开始日期。0 = 今天天气
    param['days'] = 1 # 查询天数，1 = 只查一天
    url = api + '?' + urlencode(param)
    async with aiohttp.request('get',url) as response:
        # logger.info(await response.text())
        weatherResult = await response.json()
        return {
            'code':1,
            'low':weatherResult['results'][0]['daily'][0]['low'],
            'high':weatherResult['results'][0]['daily'][0]['high'],
            'city':location
        }