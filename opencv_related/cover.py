import cv2
import numpy as np
import os

class trafficSignBroken():
    
    def __init__(self) -> None:
        pass

    def set_color(self, img):
        """
        对输入图像进行处理,现在只添加了色域转换,后面还要添加调节图片的饱和度/对比度等信息,方便进行mask的提取.
        :param img: 原始图片
        :return:  处理后的图片
        """
        kernel_size = 5
        img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        return img_hsv

    def find_mask_by_color(self, img_hsv, color):
        """
        :param img_hsv:  颜色通道转换成 HSV 之后的图片
        :param color: 需要提取的 sign 的颜色
        :return: 满足 颜色要求的 mask
        """
        if color == 'red':
            # 设置红色标志的阈
            redLower01 = np.array([0, 43, 46], dtype=np.uint8)  # 部分红
            redUpper01 = np.array([10, 255, 255], dtype=np.uint8)
            redLower02 = np.array(
                [125, 21, 31],
                dtype=np.uint8)  # 部分红  包含了紫色 棕色 # OG:125, 43, 46
            redUpper02 = np.array([180, 255, 255], dtype=np.uint8)
            red_mask01 = cv2.inRange(img_hsv, redLower01, redUpper01)
            red_mask02 = cv2.inRange(img_hsv, redLower02, redUpper02)
            mask = red_mask01 + red_mask02
        elif color == 'blue':
            Lower = np.array(
                [100, 43, 17],
                dtype=np.uint8)  # [100, 100, 46]  # og:100, 43, 46
            Upper = np.array([130, 255, 255],
                             dtype=np.uint8)  # [130, 255, 255] [124, 255, 255]
            mask = cv2.inRange(img_hsv, Lower, Upper)
        elif color == 'green':  # green should be a little lower 
            # Lower = np.array([75, 43, 22])  # [37, 43, 46] [25, 52, 72] og_now  # [65,6,22]
            # Upper = np.array([100, 255, 255])  # [102, 255, 255]                # [100,225,200]
            Lower = np.array([65,6,22])  # [37, 43, 46] [25, 52, 72] og_now  # [65,6,22]
            Upper = np.array([100,225,200])  # [102, 255, 255]                # [100,225,200]
            mask = cv2.inRange(img_hsv, Lower, Upper)
        elif color == 'gray':  # Don't change anymore
            Lower = np.array([34, 0, 0], dtype=np.uint8)
            Upper = np.array([78, 43, 30], dtype=np.uint8)  # 180, 200, 255
            mask = cv2.inRange(img_hsv, Lower, Upper)
        elif color == 'orange':  # 黄色的图片会 偏橙色 经过实验验证upper中v的分量小于200即可
            Lower = np.array([11, 15, 46], dtype=np.uint8)
            Upper = np.array([25, 255, 255], dtype=np.uint8)
            mask = cv2.inRange(img_hsv, Lower, Upper)
        elif color == 'yellow':
            #Lower = np.array([26, 100, 46], dtype=np.uint8)  # 11, 50, 50   26 #20,15,46
            #Upper = np.array([34, 255, 255], dtype=np.uint8)  # 50, 255, 255   #34,255,255
            Lower = np.array([11,15,46], dtype=np.uint8)  # 11, 50, 50   26 #20,15,46
            Upper = np.array([34, 255, 255], dtype=np.uint8)  # 50, 255, 255   #34,255,255
            mask = cv2.inRange(img_hsv, Lower, Upper)
        else:
            mask = None
        return mask

    def get_sign_area(self, img, color):
        """
        :param img:  原始的输入图片
        :param color:  需要提取的sign 的颜色
        :return: 可能是sign 的区域的坐标列表，[x, y, w, h]
        """
        img_hsv = self.set_color(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if color == 'white':
            mask = cv2.threshold(gray, 220, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        elif color == 'black':
            B, G, R = cv2.split(img)
            mask1 = cv2.threshold(B, 20, 255, cv2.THRESH_BINARY_INV)[1]
            mask2 = cv2.threshold(G, 30, 255, cv2.THRESH_BINARY_INV)[1]
            mask3 = cv2.threshold(R, 40, 255, cv2.THRESH_BINARY_INV)[1]
            temp = cv2.bitwise_and(mask1, mask2)
            mask = cv2.bitwise_and(temp, mask3)
        else:
            mask = self.find_mask_by_color(
                img_hsv, color=color)  # find the mask of a color
        return mask / 255.0

    def get_area(self, img):
        """
        得到交通标志颜色范围内的mask面积
        """
        greenMask = self.get_sign_area(img, color='green')
        redMask = self.get_sign_area(img, color='red')
        whiteMask = self.get_sign_area(img, color='white')
        blueMask = self.get_sign_area(img, color='blue')
        # yellowMask = self.get_sign_area(img, color='yellow')
        orangeMask = self.get_sign_area(img, color='orange')
        blackMask = self.get_sign_area(img, color='black')
        grayMask = self.get_sign_area(img, color='gray')

        # mask = cv2.bitwise_or(yellowMask, whiteMask)
        mask = cv2.bitwise_or(whiteMask, greenMask)
        mask = cv2.bitwise_or(mask, redMask)
        mask = cv2.bitwise_or(mask, blueMask)
        mask = cv2.bitwise_or(mask, orangeMask)
        mask = cv2.bitwise_or(mask, blackMask)
        mask = cv2.bitwise_or(mask, grayMask)

        return mask.sum()

    def traffic_detect(self, label, image, threshold=0.75):
        '''
        Judge whether the sign is covered.
        '''
        flag = False
        # 计算不同交通标志中未遮挡的颜色占整体的比例         
        if label == 'sanjiaobiaozhi':
            th = (threshold+0.15) * (1.00 / 2.00)
        elif label == 'yuanbiaozhi':
            th = threshold * (3.14 / 4.00)  # π/4
        else:
            th = threshold
        print('th:', th)
        area = image.shape[0] * image.shape[1]
        if area < 6400:
            print('ignore sign area: ', area)
            return flag,0
        maskArea = self.get_area(image)
        ratio = round(maskArea / area, 3)
        eps = 0.00001
        if ratio < th - eps:
            flag = True
        return flag,ratio

    def preprocess_filter(self, img_path):
        '''
            filter the traffic signs from two rules:
            1. avg_r > 200 avg_g > 200 avg_b > 200 or ang_v > 150
            2. traffic sign is not captured completly
        '''
        image_bgr = cv2.imread(img_path)
        ## houchuli 过滤
        b,g,r = cv2.split(image_bgr)
        b_list = [m for i in b for m in i]
        g_list = [m for i in g for m in i]
        r_list = [m for i in r for m in i]
        avg_b = sum(b_list)/len(b_list)
        avg_g = sum(g_list)/len(g_list)
        avg_r = sum(r_list)/len(r_list)
        if avg_b > 200 and avg_g > 200 and avg_r > 200:
            print("the avg of rgb are bigger than 200")
            return None
        image_hsv = cv2.cvtColor(image_bgr,cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(image_hsv)
        v_list = [m for i in v for m in i]
        avg_v = sum(v_list)/len(v_list)
        if avg_v >150:
            print("the avg of v is bigger than 150")
            return None
        return image_bgr
    
def run_folder(folder):
    broken_det = trafficSignBroken()
    for img in os.listdir(folder):
        img_path = os.path.join(folder,img)
        print(img_path)
        image_bgr = broken_det.preprocess_filter(img_path)
        if image_bgr is not None:
            flag,ratio = broken_det.traffic_detect( "jiaotongbiaozhi", image_bgr, threshold=0.75)
        else:
            flag,ratio = False,0
            
        if flag is True:
            cv2.imwrite(os.path.join("crop_save",img),image_bgr)
            print(f"flag: {flag}, ratio: {ratio}, img_path: {img_path}")

def run_path(img_path):
    broken_det = trafficSignBroken()
    image_bgr = cv2.imread(img_path)
    ## houchuli 过滤
    b,g,r = cv2.split(image_bgr)
    b_list = [m for i in b for m in i]
    g_list = [m for i in g for m in i]
    r_list = [m for i in r for m in i]
    avg_b = sum(b_list)/len(b_list)
    avg_g = sum(g_list)/len(g_list)
    avg_r = sum(r_list)/len(r_list)
    if avg_b > 200 and avg_g > 200 and avg_r > 200:
        print(""" avg_b > 200 and avg_g > 200 and avg_r > 200 """)
    image_hsv = cv2.cvtColor(image_bgr,cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(image_hsv)
    v_list = [m for i in v for m in i]
    avg_v = sum(v_list)/len(v_list)
    if avg_v >150:
        print(""" avg_v >150 """)
    flag,ratio = broken_det.traffic_detect( "jiaotongbiaozhi", image_bgr, threshold=0.75)
    
    print(f"flag: {flag}, ratio: {ratio}, img_path: {img_path}")

if __name__ == '__main__':
    # run_folder("crop_img")
    img_path = r"C:\Users\14520\Downloads\123.jpg"
    run_path(img_path)
 