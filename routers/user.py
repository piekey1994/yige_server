from fastapi import APIRouter,Form
from my_config import default_config
from db.user_model import UserModel

router = APIRouter()

@router.post('/weapp/user/setsex')
async def setsex(openid:str=Form(),sex:int=Form()):

    await UserModel.setSex(openid,sex)
    return 'true:1'


@router.post('/weapp/user/setage')
async def setage(openid:str=Form(),age:int=Form()):

    await UserModel.setAge(openid,age)
    return 'true:1'

