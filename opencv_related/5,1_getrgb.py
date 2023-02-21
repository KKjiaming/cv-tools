import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

b_all= []
g_all= []
r_all= []

b_avg= []
g_avg= []
r_avg= []

h_all= []
s_all= []
v_all= []

h_avg= []
s_avg= []
v_avg= []


def draw_distribution_histogram(nums, path, is_hist=True, is_kde=True, is_rug=False, \
  is_vertical=False, is_norm_hist=True):
  """

  bins: 设置直方图条形的数目
  is_hist: 是否绘制直方图
  is_kde: 是否绘制核密度图
  is_rug: 是否绘制生成观测数值的小细条
  is_vertical: 如果为True，观察值在y轴上
  is_norm_hist: 如果为True，直方图高度显示一个密度而不是一个计数，如果kde设置为True，则此参数一定为True
  """
  sns.set()  #切换到sns的默认运行配置
  sns.distplot(nums, bins=10, hist=is_hist, kde=is_kde, rug=is_rug, \
    hist_kws={"color":"steelblue"}, kde_kws={"color":"purple"}, \
    vertical=is_vertical, norm_hist=is_norm_hist)
  #添加x轴和y轴标签
  plt.xlabel("XXX")
  plt.ylabel("YYY")

  #添加标题
  plt.title("Distribution")
  plt.tight_layout()  # 处理显示不完整的问题
  plt.savefig(path, dpi=300)

# x=np.random.randn(100)
# path = "distribution.jpg"
# draw_distribution_histogram(x, '1.jpg', True, True)
def hsv_histomgram(img_hsv,img_rgb,img_path):
  h,s,v = cv2.split(img_hsv)
  h_list = [m for i in h for m in i]
  s_list = [m for i in s for m in i]
  v_list = [m for i in v for m in i]
  # draw_distribution_histogram(np.array(b_list),'1.jpg', True, True)
  avg_h = sum(h_list)/len(h_list)
  avg_s = sum(s_list)/len(s_list)
  avg_v = sum(v_list)/len(v_list)
  
  # plt.figure(figsize=(8, 8))
  # plt.subplot(2, 2, 1)
  # plt.imshow(img_rgb)
  # plt.title("img")
  # plt.subplot(2, 2, 2)
  # plt.hist(np.array(h_list), bins=10, facecolor="blue", edgecolor="black", alpha=0.7)
  # plt.title("avg H: "+str(avg_h))
  # plt.subplot(2, 2, 3)
  # plt.hist(np.array(s_list), bins=10, facecolor="red", edgecolor="black", alpha=0.7)
  # plt.title("avg S: "+str(avg_s))
  # plt.subplot(2, 2, 4)
  # plt.hist(np.array(v_list), bins=10, facecolor="green", edgecolor="black", alpha=0.7)
  # plt.title("avg V: "+str(avg_v))
  
  # plt.show()
  # plt.savefig( os.path.join("threshold_problem\\hsv",img_path.split('\\')[-1])  , dpi=300)
  
  return h_list,s_list,v_list,avg_h,avg_s,avg_v

def rgb_histomgram(img_bgr,img_rgb,img_path):
  b,g,r = cv2.split(img_bgr)
  b_list = [m for i in b for m in i]
  g_list = [m for i in g for m in i]
  r_list = [m for i in r for m in i]
  # draw_distribution_histogram(np.array(b_list),'1.jpg', True, True)
  avg_b = sum(b_list)/len(b_list)
  avg_g = sum(g_list)/len(g_list)
  avg_r = sum(r_list)/len(r_list)
  
  # plt.figure(figsize=(8, 8))
  # plt.subplot(2, 2, 1)
  # plt.imshow(img_rgb)
  # plt.title("img")
  # plt.subplot(2, 2, 2)

  # plt.hist(np.array(b_list), bins=10, facecolor="blue", edgecolor="black", alpha=0.7)

  # plt.title("avg B: "+str(avg_b))

  # plt.subplot(2, 2, 3)
  # plt.hist(np.array(g_list), bins=10, facecolor="green", edgecolor="black", alpha=0.7)

  # plt.title("avg G: "+str(avg_g))

  # plt.subplot(2, 2, 4)
  # plt.hist(np.array(r_list), bins=10, facecolor="red", edgecolor="black", alpha=0.7)

  # plt.title("avg R: "+str(avg_r))
  # plt.show()
      
  # plt.savefig( os.path.join("threshold_problem\\rgb",img_path.split('\\')[-1])  , dpi=300)
  return r_list,g_list,b_list,avg_r,avg_g,avg_b

def histogram(h_avg,s_avg,v_avg,mode):
  if "hsv" in mode :
        title_1 = "h"
        title_2 = "s"
        title_3 = "v"
  elif "rgb" in mode:
        title_1 = "r"
        title_2 = "g"
        title_3 = "b"
        
  plt.figure()
  plt.subplot(3, 1, 1)
  plt.hist(np.array(h_avg), bins=10, facecolor="red", edgecolor="black", alpha=0.7)
  plt.title(title_1)
  
  plt.subplot(3, 1, 2)
  plt.hist(np.array(s_avg), bins=10, facecolor="green", edgecolor="black", alpha=0.7)
  plt.title(title_2)

  plt.subplot(3, 1, 3)
  plt.hist(np.array(v_avg), bins=10, facecolor="blue", edgecolor="black", alpha=0.7)
  plt.title(title_3)
  # plt.show()
  plt.savefig(os.path.join("threshold_problem\\",mode)  , dpi=300)


import numpy as np  
import matplotlib.pyplot as plt

folder_path = r'threshold_problem'
color = ['c', 'b', 'g', 'r', 'm', 'y', 'k', 'w']

for img in os.listdir(folder_path):
        if not 'jpg' in img:
              continue
        print(img)
        img_path = os.path.join(folder_path,img)
        img_bgr = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)
        img_hsv = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
        h_list,s_list,v_list,avg_h,avg_s,avg_v = hsv_histomgram(img_hsv,img_rgb,img_path)
        r_list,g_list,b_list,avg_r,avg_g,avg_b = rgb_histomgram(img_bgr,img_rgb,img_path)
        
        h_all+=h_list
        s_all+=s_list
        v_all+=v_list
        
        r_all+=r_list
        g_all+=g_list
        b_all+=b_list
        
        h_avg+= [avg_h]
        s_avg+= [avg_s]
        v_avg+= [avg_v]
        
        r_avg+= [avg_r]
        g_avg+= [avg_g]
        b_avg+= [avg_b]

histogram(h_avg,s_avg,v_avg,"avg_hsv.jpg")
histogram(r_avg,g_avg,b_avg,"avg_rgb.jpg")
histogram(h_all,s_all,v_all,"total_hsv.jpg")
histogram(r_all,g_all,b_all,"total_rgb.jpg")

print("---")