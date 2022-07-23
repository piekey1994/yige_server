from fastapi import APIRouter,File,UploadFile
from typing import Optional
from my_config import default_config
import aiofiles
from uuid import uuid4

router = APIRouter()

async def uploadToBucket(filedata):
    '''
    上传文件到云服务器
    返回文件url
    '''
    pass

@router.post('/weapp/upload')
async def upload(file:UploadFile):
    content_type = file.content_type
    if content_type not in ['image/jpeg','image/jpg','image/png']:
        return {
            'code':0,
            'error':'不支持的上传图片类型：{}'.format(content_type)
        }
    max_size =default_config['upload']['max_size'] * 1024 * 1024
    
    file_data = await file.read(max_size+1)
    if len(file_data)>max_size:
        return {
            'code':0,
            'error':'上传图片过大，仅支持 5M 以内的图片上传'
        }
    else:
        filename = '{}.{}'.format(uuid4(),content_type[content_type.find('/')+1:])
        save_path = default_config['upload']['save_path']
        host = default_config['upload']['url']
        async with aiofiles.open('{}/{}'.format(save_path,filename),'wb') as input_file:
            await input_file.write(file_data)
            return {
                'code':1,
                'data':{
                    'imgUrl': '{}/{}'.format(host,filename),
                    'size': len(file_data),
                    'mimeType': content_type,
                    'name':filename
                }
            }
    
    
