import joblib 
from skimage.feature import hog
from skimage import io,transform
from my_config import default_config
from skimage.color import gray2rgb
import numpy as np

img=io.imread(r'D:\项目\小程序比赛\服装分类\python\图\裤子长裤\2.jpg')
if len(img.shape)==2:
    img= gray2rgb(img)
print(img.shape)
r = np.mean(img[int(img.shape[0]*0.25):int(img.shape[0]*0.75),int(img.shape[1]*0.25):int(img.shape[1]*0.75),0])
g = np.mean(img[int(img.shape[0]*0.25):int(img.shape[0]*0.75),int(img.shape[1]*0.25):int(img.shape[1]*0.75),1])
b = np.mean(img[int(img.shape[0]*0.25):int(img.shape[0]*0.75),int(img.shape[1]*0.25):int(img.shape[1]*0.75),2])
print(r,g,b)