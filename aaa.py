import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def main():
    header = {  # 模拟浏览器头部信息
        'user-agent': '[Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3185 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/6210 MicroMessenger/8.0.16.2040(0x2800105F) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64] Edg/98.0.4758.102'

    }
    async with aiohttp.request(
        'get',
        # 'https://m.tb.cn/h.UaupYeM?tk=TvFO2tinJvf',
        'https://main.m.taobao.com/detail/index.html?id=671922508521&downgrade_from=ssr&bxsign=scdlt1OiEdno8tvXcTdAI4dQHQi6AggM_8Jw66GmvnPQI80xtwIgQGvR7seqAaAbkrnmFBClgnWGeb3LYWTwY3xzmzSPxLFYlJlH-xXPpgOs2COR-xlVMi1VKQnzCNKirMa&short_name=h.UaupYeM&un=1bf862be87f6e9122040bd82ddc2e1ea&app=weixin&bc_fl_src=share-104909552135421-2-1&cpp=1&share_crt_v=1&shareurl=true&sp_abtk=gray_1_code_simpleAndroid&sp_tk=VHZGTzJ0aW5KdmY=&spm=a2159r.13376460.0.0&tbSocialPopKey=shareItem&tk=TvFO2tinJvf&un_site=0&ut_sk=1.XvvVkMGOqu4DACaVT6wio5ZS_21646297_1660443382516.TaoPassword-WeiXin.1&detail_downgrade_from=true',
        headers=header
    ) as response:
        wb_data = await response.text()
        # print(wb_data)
        soup = BeautifulSoup(wb_data,'lxml')
        for img in soup.find_all('img'):
            print(img.attrs['src'])

asyncio.get_event_loop().run_until_complete(main())