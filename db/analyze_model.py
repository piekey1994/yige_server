from db.db import AsyncDB

class AnalyzeModel(object):
    @classmethod
    async def getTypeData(cls,openid):
        sql = '''
        select 
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothetype=0 ) as shangyi,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothetype=1 ) as kuzi,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothetype=2 ) as waitao,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothetype=3 ) as qunzi,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothetype=3 ) as xiezi,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothetype=4 ) as qita
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,[openid for _ in range(6)])
                r = await cur.fetchall()
                return r

    @classmethod
    async def getSeasonData(cls,openid):
        sql='''
        select 
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clotheseason=0 ) as chunqiu,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clotheseason=1 ) as xia,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clotheseason=2 ) as dong,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clotheseason=2 ) as quannian
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,[openid for _ in range(4)])
                r = await cur.fetchall()
                return r

    @classmethod
    async def getColorData(cls,openid):
        sql='''
        select 
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=0 ) as hei,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=1 ) as bai,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=2 ) as hui,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=3 ) as hong,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=4 ) as zong,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=0 ) as hei,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=5 ) as cheng,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=6 ) as huang,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=7 ) as lv,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=8 ) as lan,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=0 ) as hei,
        (select count(*) from clothespress,clothe WHERE clothespress.openid=%s AND clothe.clotheid=clothespress.clotheid AND clothe.location=0 AND clothe.clothecolor=9 ) as zi
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                # print(sql,[openid for _ in range(12)])
                await cur.execute(sql,[openid for _ in range(12)])
                r = await cur.fetchall()
                return r