from db.db import AsyncDB

class MatchModel(object):
    @classmethod
    async def addMatch(cls,uid,cids,img):
        sql='''
        insert into selfmatch(
            uid,
            img
        ) values(%s,%s)
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(
                    uid,
                    img
                ))
                sid = conn.insert_id()
                datalist=[]
                for cid in cids:
                    datalist.append((sid,cid))
                sql="insert into matchdetail(sid,cid) values(%s,%s)"
                await cur.executemany(sql,datalist)
                await conn.commit()
                return sid

    @classmethod
    async def addPic(cls,sid,img):
        sql = '''
        update selfmatch set img=%s where id=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(img,sid))
                await conn.commit()
    
    @classmethod
    async def addDetail(cls,sid,weather,situation,detail):
        sql = '''
        update selfmatch set weather=%s, situation=%s, detail=%s where id=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(weather,situation,detail,sid))
                await conn.commit()
    
    @classmethod
    async def getMatch(cls,uid):
        sql = 'SELECT * FROM selfmatch WHERE uid=%s'
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(uid))
                r = await cur.fetchall()
                return r
    
    @classmethod
    async def getMatch(cls,sid):
        sql = 'SELECT * FROM selfmatch WHERE id=%s'
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(sid))
                r = await cur.fetchall()
                return r

    @classmethod
    async def getImgs(cls,sid):
        sql = '''
        select clothe.clotheid, clothe.clotheimg from matchdetail,clothe 
        WHERE matchdetail.sid=%s and matchdetail.cid=clothe.clotheid
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(sid))
                r = await cur.fetchall()
                return r
    
    @classmethod
    async def deleteMatch(cls,sid,uid):
        sql = '''
        DELETE FROM selfmatch WHERE uid=%s AND %s=id
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(uid,sid))
                await conn.commit()
