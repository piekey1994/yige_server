from db.db import AsyncDB

class UserModel(object):

    @classmethod
    async def registerUser(cls,openid,name,sex):
        sql = '''
        SELECT * FROM user WHERE openid=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(openid))
                r = await cur.fetchall()
                if len(r)==0:
                    sql='''
                    insert into user(
                        openid,
                        nickname,
                        sex
                    ) values(%s,%s,%s)
                    '''
                    await cur.execute(sql,(
                        openid,
                        name,
                        sex
                    ))
                    await conn.commit()
    
    @classmethod
    async def getInfo(cls,openid):
        sql = 'SELECT * FROM user WHERE openid=%s'
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(openid))
                r = await cur.fetchone()
                return r
    
    @classmethod
    async def setAge(cls,openid,age):
        sql = '''
        update user set age=%s where openid=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(age,openid))
                await conn.commit()
    
    @classmethod
    async def setAge(cls,openid,sex):
        sql = '''
        update user set sex=%s where openid=%s
        '''
        async with AsyncDB.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql,(sex,openid))
                await conn.commit()
    