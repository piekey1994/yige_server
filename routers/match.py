from fastapi import APIRouter,Form
from my_config import default_config
from db.clothe_model import ClotheModel
from db.match_model import MatchModel

router = APIRouter()

@router.post('/weapp/match/uploadCids')
async def getMyLike(cids:str=Form(),uid:str=Form()):
    # //接收post请求，cid列表，用户id
    # //新建搭配，并添加cid列表

    # //返回成功确认结果
    cids = cids.split()
    img = await ClotheModel.getClothe(int(cids[0]))
    img = img['clotheimg']
    res = await MatchModel.addMatch(uid,cids,img)
    return str(res)

@router.post('/weapp/match/uploadPic')
async def uploadPic(sid:str=Form(),img:str=Form()):
    # //接收请求，是否有图，图片地址，sid
    # //如果有图则将图片写入sid项目中
    # //返回确认信息
    await MatchModel.addPic(sid,img)
    return '1'

@router.post('/weapp/match/uploadDetail')
async def uploadDetail(sid:str=Form(),weather:int=Form(),situation:str=Form(),detail:str=Form()):
    # //接收请求，温度，场景，详情
    # //写入数据库
    # //返回确认信息
    await MatchModel.addDetail(sid,weather,situation,detail)
    return '1'

@router.post('/weapp/match/getMatch')
async def getMatch(uid:str=Form()):
    # //接受请求，用户id
    # //读取数据库穿搭列表
    # //返回给用户
    result = await MatchModel.getMatch(uid)
    return {
        'code':1,
        'data':result,
        'length':len(result)
    }

@router.post('/weapp/match/getMatchDetail')
async def getMatchDetail(sid:str=Form()):
    # //接收请求，sid
    # //读取搭配列表和详情
    # //返回给用户
    result = await MatchModel.getDetail(sid)
    imgs = await MatchModel.getImgs(sid)
    return {
        'code':1,
        'data':result,
        'imgs':imgs
    }

@router.post('/weapp/match/deleteMatch')
async def deleteMatch(sid:str=Form(),uid:str=Form()):

    await MatchModel.deleteMatch(sid,uid)
    return 'true:1'