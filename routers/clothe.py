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


@router.post('/weapp/clothe/clotheDetail')
async def clotheDetail(clotheid:str=Form()):
    clothedata = await ClotheModel.getclothe(clotheid)
    recommendData = await ClotheModel.getRecommend(clotheid)
    del clothedata['hog']
    return {
        'code':1,
        'data':clothedata,
        'recommendData':recommendData
    }


@router.post('/weapp/clothe/recommendDetail')
async def recommendDetail(ri:str=Form(),rj:str=Form(),rk:str=Form(),openid:str=Form()):
    myAllClothes = await ClotheModel.getAll(openid)
    recommendArray = []
    for new_type,ifs_dict in ifashion_pkl.items():
        for (i,j,k),res_dict in ifs_dict.items():
            if i==ri and j!=rj and k==rk:
                tempFeatureArray=[]
                for clothe in myAllClothes:
                    rgb = np.array((clothe['r'],clothe['g'],clothe['b']))
                    hog = np.frombuffer(clothe['hog'],dtype=np.float16)
                    if new_type==clothe['clothetype'] and \
                        np.sum(np.power((rgb-res_dict['rgb']),2))<3000:
                        hog_dist =np.sum(np.power((hog-res_dict['hog']),2))
                        if hog_dist<31:
                            tempFeature={
                                'cid':clothe['clotheid'],
                                'img':clothe['clotheimg'],
                                'distance':hog_dist
                            }
                            tempFeatureArray.append(tempFeature)
                sort_tfa = sorted(tempFeatureArray,key=lambda x:x['distance'])
                recommendArray.append(sort_tfa[:3])
    if len(recommendArray)>0:
        return {
            'code':1,
            'recommends':recommendArray
        }
    else:
        return {
            'code':0,
            'error':'你衣服太少了'
        }

@router.post('/weapp/clothe/getMyLike')
async def getMyLike(openid:str=Form()):
    all = await ClotheModel.getMyLike(openid)
    return {
        'code':1,
        'data':all,
        'length':len(all)
    }

@router.post('/weapp/clothe/getAll')
async def getAll(openid:str=Form()):
    all = await ClotheModel.getAll2(openid)
    return {
        'code':1,
        'data':all,
        'length':len(all)
    }

@router.post('/weapp/clothe/setlocation')
async def setlocation(clotheid:str=Form(),location:int=Form()):
    await ClotheModel.setlocation(clotheid,location)
    return 'true:1'

@router.post('/weapp/clothe/setType')
async def setType(clotheid:str=Form(),clothetype:int=Form()):
    await ClotheModel.settype(clotheid,clothetype)
    return 'true:1'

@router.post('/weapp/clothe/setDetail')
async def setDetail(clotheid:str=Form(),clothedetail:str=Form()):
    await ClotheModel.setdetail(clotheid,clothedetail)
    return 'true:1'

@router.post('/weapp/clothe/setSeason')
async def setSeason(clotheid:str=Form(),clotheseason:int=Form()):
    await ClotheModel.setseason(clotheid,clotheseason)
    return 'true:1'

@router.post('/weapp/clothe/setColor')
async def setColor(clotheid:str=Form(),clothecolor:int=Form()):
    await ClotheModel.setcolor(clotheid,clothecolor)
    return 'true:1'

@router.post('/weapp/clothe/setStar')
async def setStar(clotheid:str=Form(),clothestar:float=Form()):
    await ClotheModel.setstar(clotheid,clothestar)
    return 'true:1'


@router.post('/weapp/clothe/delete')
async def delete_clothe(openid:str=Form(),clotheid:str=Form()):
    await ClotheModel.delete(openid,clotheid)
    return 'true:1'

@router.post('/weapp/clothe/getSeasonClothe')
async def getSeasonClothe(openid:str=Form(),season:str=Form()):
    if season=='春秋装':
        seasonkey=0
    if season=='春秋装+薄外套':
        seasonkey=0
    if season=='夏装':
        seasonkey=1
    if season=='冬装':
        seasonkey=2
    if season=='冬装+外套':
        seasonkey=2
    result = await ClotheModel.getSeasonClothe(openid,seasonkey)
    return {
        'code':1,
        'data':result,
        'length':len(result)
    }

@router.post('/weapp/clothe/getResult')
async def getResult(
    openid:str=Form(),
    value:str=Form(),
    currentTab:int=Form(),
    keys:str=Form()
):
    keys = keys.split(',')
    seasonflag = 0
    colorflag = 0
    typeflag = 0
    for key in keys:
        if key == '春':
            seasonkey=0
            seasonflag+=1
        elif key == '夏':
            seasonkey=1
            seasonflag+=1
        elif key == '秋':
            seasonkey=0
            seasonflag+=1
        elif key == '冬':
            seasonkey=2
            seasonflag+=1
        elif key == '上衣':
            typekey=0
            typeflag+=1
        elif key == '裤子':
            typekey=1
            typeflag+=1
        elif key == '外套':
            typekey=2
            typeflag+=1
        elif key == '裙子':
            typekey=3
            typeflag+=1
        elif key == '鞋子':
            typekey=4
            typeflag+=1
        elif key == '其他':
            typekey=5
            typeflag+=1
        elif key == '黑':
            colorkey=0
            colorflag+=1
        elif key == '白':
            colorkey=1
            colorflag+=1
        elif key == '灰':
            colorkey=2
            colorflag+=1
        elif key == '红':
            colorkey=3
            colorflag+=1
        elif key == '棕':
            colorkey=4
            colorflag+=1
        elif key == '橙':
            colorkey=5
            colorflag+=1
        elif key == '黄':
            colorkey=6
            colorflag+=1
        elif key == '绿':
            colorkey=7
            colorflag+=1
        elif key == '蓝':
            colorkey=8
            colorflag+=1
        elif key == '紫':
            colorkey=9
            colorflag+=1
        if  seasonflag != 1:
            seasonkey = -1
        if  colorflag != 1:
            colorkey = -1
        if  typeflag != 1:
            typekey = -1
    result = await ClotheModel.getResult(
        openid, value, currentTab, seasonkey, colorkey, typekey
    )
    return {
        'code':1,
        'data':result,
        'length':len(result)
    }