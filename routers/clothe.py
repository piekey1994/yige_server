from fastapi import APIRouter,Form
from my_config import default_config
from db.clothe_model import ClotheModel
from svm_server import SvmModel
import pickle
import numpy as np

router = APIRouter()
ifashion_pkl:dict = pickle.load(open(default_config['model']['ifashion_path'],'wb'))

@router.post('/weapp/clothe/getMyLike')
async def getMyLike(openid:str=Form()):
    all = await ClotheModel.getMyLike(openid)
    return {
        'code':1,
        'data':all,
        'len':len(all)
    }

@router.post('/weapp/clothe/addClothe')
async def addClothe(openid:str=Form(),url:str=Form(),title:str=Form()):
    if not url.startswith(default_config['upload']['url']): #只支持本地已存的图片
        return {
            'code':0,
            'error':'图片路径错误'
        }
    filename = url[url.rfind('/')+1:]
    filePath = '{}/{}'.format(default_config['upload']['save_path'],filename)
    
    svm_model = SvmModel(filePath)

    if title != '暂无描述':
        if title.find('上衣')!=-1 or title.find('短袖')!=-1 or title.find('长袖')!=-1:
            clothe_type = 0
        elif title.find('裤')!=-1:
            clothe_type = 1
        elif title.find('外套')!=-1:
            clothe_type = 2
        elif title.find('裙')!=-1:
            clothe_type = 3
        elif title.find('鞋')!=-1:
            clothe_type = 4
        else:
            clothe_type = 5

        if title.find('夏')!=-1 or title.find('短袖')!=-1:
            season = 1
        elif title.find('冬')!=-1 or title.find('长袖')!=-1:
            season = 2
        else:
            season = 3
    else:
        clothe_class = svm_model.gettype()
        if clothe_class == 0:
            clothe_type = 3
            season = 1
        elif clothe_class == 1:
            clothe_type = 1
            season = 1
        elif clothe_class == 2:
            clothe_type = 1
            season = 2
        elif clothe_class == 3:
            clothe_type = 0
            season = 1
        elif clothe_class == 4:
            clothe_type = 0
            season = 2
        elif clothe_class == 5:
            clothe_type = 2
            season = 2
        elif clothe_class == 6:
            clothe_type = 4
            season = 3
    
    color,r,g,b = svm_model.getColorNum()
    cid = await ClotheModel.addclothe(openid, url, title, clothe_type, color, season,r,g,b)
    return {
        'code':1,
        'cid':cid,
        'filepath':filePath
    }

@router.post('/weapp/clothe/getRecommend')
async def getRecommend(clotheid:str=Form(),filepath:str=Form()):
    clothe = await ClotheModel.getclothe(clotheid)
    svm_model = SvmModel(filepath)
    hog = svm_model.calHog()
    await ClotheModel.setHog(clotheid,hog)
    rgb = np.array((clothe['r'],clothe['g'],clothe['b']))
    clothe_type = clothe['clothetype']
    type_dict:dict = ifashion_pkl['clothe_type']
    #取颜色方差小于3000切hog差值小于31的前3个加入数据库
    hogtemp ={}
    for ijk,value_dict in type_dict.items():
        if np.sum(np.power((rgb-value_dict['rgb']),2))<3000:
            hog_dist =np.sum(np.power((hog-value_dict['hog']),2))
            if hog_dist<31:
                hogtemp[ijk]=hog_dist
    hogtemp = sorted(hogtemp.items(),key=lambda x:x[1])
    for ijk,dist in hogtemp[:3]:
        i,j,k=ijk
        await ClotheModel.addRecommend(clotheid,i,j,k)
    return 'finish'