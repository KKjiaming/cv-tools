import os
import cv2
import matplotlib.pyplot as plt

folder_path = r'camera_proplem'
color = ['c', 'b', 'g', 'r', 'm', 'y', 'k', 'w']

h_all= []
s_all= []
v_all= []

for img in os.listdir(folder_path):
    img_path = os.path.join(folder_path,img)
    image = cv2.imread(img_path)
    img_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(img_hsv)
    # print(v)
    h_all.append(sum(map(sum,h))/(h.shape[0]*h.shape[1]))
    s_all.append(sum(map(sum,s))/(s.shape[0]*s.shape[1]))
    v_all.append(sum(map(sum,v))/(v.shape[0]*v.shape[1]))
    
print(v_all)

plt.bar(range(len(h_all)), h_all,color=color[0])
plt.show()

plt.bar(range(len(s_all)), s_all,color=color[0])
plt.show()
plt.bar(range(len(v_all)), v_all,color=color[0])
plt.show()
    
    
    
    