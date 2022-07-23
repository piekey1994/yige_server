import joblib 
from skimage.feature import hog
from skimage import io,transform
from my_config import default_config
from skimage.color import gray2rgb,rgb2gray,rgba2rgb
import numpy as np

standardColor_map={
    (0,0,0):0,#黑0
    (255,255,255):1,#白1
    (128,128,128):2,#灰2
    (255,0,0):3,#红3
    (255,120,120):3,#红4
    (139,69,19):4,#棕5
    (96,36,26):4,#棕6
    (255,165,0):5,#橙7
    (255,80,0):5,#橙8
    (255,255,0):6,#黄9
    (255,255,125):6,#黄10
    (0,128,0):7,#绿11
    (0,255,0):7,#绿12
    (0,0,255):8,#蓝13
    (0,255,255):8,#蓝14
    (128,0,128):9,#紫15
    (190,70,190):9,#紫16
}

class SvmModel(object):
    svm_model = joblib.load(default_config['model']['svm_path'])

    def __init__(self,filepath):
        self.img = io.imread(filepath)
        if len(self.img.shape)>3:
            self.img=rgba2rgb(self.img)

    def calHog(self):
        if len(self.img.shape)>2:
            gray_img = rgb2gray(self.img)
        else:
            gray_img = self.img
        dst=transform.resize(gray_img,(64,64))
        fd = hog(dst, orientations=9, pixels_per_cell=(8, 8),cells_per_block=(2, 2))
        return fd.astype(np.float16)

    def gettype(self):
        hog=self.calHog()
        result=self.svm_model.predict([hog])
        return result[0]

    def getColorNum(self):
        if len(self.img.shape)==2:
            img= gray2rgb(self.img)
        else:
            img = self.img
        x_begin = int(img.shape[0]*0.25)
        x_end = int(img.shape[0]*0.75)
        y_begin = int(img.shape[1]*0.25)
        y_end = int(img.shape[1]*0.75)
        r = np.mean(img[x_begin:x_end,y_begin:y_end,0])
        g = np.mean(img[x_begin:x_end,y_begin:y_end,1])
        b = np.mean(img[x_begin:x_end,y_begin:y_end,2])
        avg_color=(r,g,b)
        sort_color = sorted(
            standardColor_map.items(),
            key = lambda x: np.sum(np.power((np.array(x[0])-np.array(avg_color)),2)),
            reverse=False
        )
        return sort_color[0][1],int(r),int(g),int(b)
