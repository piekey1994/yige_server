from db.db import AsyncDB
import numpy as np

class ClotheModel(object):

    @classmethod
    async def addclothe(cls,openid,url,title,type,color,season,r,g,b):
        sql='''
        insert into clothe(
            clotheimg,
            clothedetail,
            clothetype,
            clothecolor,
            clotheseason,
            r,
            g,
            b
        ) values(%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(
                    url,
                    title,
                    type,
                    color,
                    season,
                    r,
                    g,
                    b
                ))
                cid = conn.insert_id()
                sql = '''
                insert into clothespress(openid,clotheid) values(%s,%s)
                '''
                await cur.execute(sql,(openid,cid))
                await conn.commit()
                return cid

    @classmethod
    async def setHog(cls,clotheid,hog:np.ndarray):

        vector = np.asarray(hog,dtype=np.float16).tostring()

        sql = '''
        update clothe set hog="%s" where clotheid=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(vector,clotheid))
                await conn.commit()

    @classmethod
    async def addRecommend(cls,clotheid,i,j,k):
        sql='''
        insert into clotherecommend(
            clotheid,
            i,
            j,
            k
        ) values(%s,%s,%s,%s)
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(clotheid,i,j,k))
                await conn.commit()
    
    @classmethod
    async def getRecommend(cls,clotheid):
        sql = 'SELECT i,j,k FROM clotherecommend WHERE clotheid=%s'
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(clotheid))
                r = await cur.fetchall()
                return r

    @classmethod
    async def getclothe(cls,clotheid):
        sql = 'SELECT * FROM clothe WHERE clotheid=%s'
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(clotheid))
                r = await cur.fetchone()
                return r

    @classmethod
    async def setlocation(cls,clotheid,location):
        sql = '''
        update clothe set location=%s where clotheid=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(location,clotheid))
                await conn.commit()

    @classmethod
    async def settype(cls,clotheid,type):
        sql = '''
        update clothe set clothetype=%s where clotheid=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(type,clotheid))
                await conn.commit()
    
    @classmethod
    async def setseason(cls,clotheid,season):
        sql = '''
        update clothe set clotheseason=%s where clotheid=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(season,clotheid))
                await conn.commit()
    
    @classmethod
    async def setcolor(cls,clotheid,color):
        sql = '''
        update clothe set clothecolor=%s where clotheid=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(color,clotheid))
                await conn.commit()
    
    @classmethod
    async def setstar(cls,clotheid,key):
        sql = '''
        update clothe set clothestar=%s where clotheid=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(key,clotheid))
                await conn.commit()
    
    @classmethod
    async def setdetail(cls,clotheid,detail):
        sql = '''
        update clothe set clothedetail=%s where clotheid=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(detail,clotheid))
                await conn.commit()

    @classmethod
    async def getAll(cls,openid):
        sql = '''
        SELECT clothe.* FROM clothe , clothespress 
        WHERE openid=%s AND clothe.clotheid=clothespress.clotheid
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(openid))
                r = await cur.fetchall()
                return r
    
    @classmethod
    async def getAll2(cls,openid):
        sql = '''
        SELECT clothe.clothetype, clothe.location,clothe.clotheid,
        clothe.clotheimg,clothe.clothedetail FROM clothe , clothespress 
        WHERE openid=%s AND clothe.clotheid=clothespress.clotheid
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(openid))
                r = await cur.fetchall()
                return r

    @classmethod
    async def getMyLike(cls,openid):
        sql = '''
        SELECT clothe.clotheid as cid,clothe.clotheimg as img FROM clothe ,
         clothespress WHERE openid=%s AND 
         clothe.clotheid=clothespress.clotheid AND 
         clothe.location=1 ORDER BY clothe.clothestar DESC LIMIT 0,5
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(openid))
                r = await cur.fetchall()
                return r

    @classmethod
    async def delete(cls,openid,clotheid):
        sql = '''
        DELETE FROM clothespress WHERE openid=%s 
        AND %s=clothespress.clotheid
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(openid,clotheid))
                await conn.commit()

    @classmethod
    async def getResult(cls,openid,value,location,seasonkey,colorkey,typekey):
        q1 = '''SELECT clothe.clothetype, clothe.location,clothe.clotheid,
        clothe.clotheimg,clothe.clothedetail FROM clothe , clothespress 
        WHERE openid=%s AND clothe.clotheid=clothespress.clotheid 
        AND clothe.location=%s AND ('''
        q2="1"
        q3="1"
        q4="1"
        q5=" OR clothe.clothedetail like '%"+value+"%')"
        if colorkey != -1:
            q2="clothe.clothecolor=%s "
        if seasonkey != -1:
            q3="clothe.clotheseason=%s "
        if typekey != -1:
            q4 = "clothe.clothetype=%s "
        if colorkey==-1 and seasonkey==-1 and typekey==-1:
            q5=" AND  clothe.clothedetail like '%"+value+"%')"
        q = q1+q2+' AND '+q3+' AND '+q4+q5
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(q,(
                    openid,
                    location,
                    colorkey,
                    seasonkey,
                    typekey
                ))
                r = await cur.fetchall()
                return r
    
    @classmethod
    async def getSeasonClothe(cls,openid, seasonkey):
        sql = '''
        SELECT clothe.clotheid as cid,clothe.clotheimg as img 
        FROM clothe , clothespress WHERE openid=%s 
        AND clothe.clotheid=clothespress.clotheid AND 
        clothe.location=0 AND clothe.clotheseason=%s
        ORDER BY clothe.clothestar DESC LIMIT 0,6
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(openid,seasonkey))
                r = await cur.fetchall()
                return r