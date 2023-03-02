import cv2
import numpy as np

img_path = "/dataset/result/asset_detect_v0.6.0/巡检测试集/交通资产测试集/quchong/gonglizhuang/2/11541_2023-02-21_15-30-34-164.jpg"
img_bgr = cv2.imread(img_path)
# breakpoint()
cv2.line(img_bgr,(200,0),(200,2056),(255,0,0),5)
cv2.line(img_bgr,(2264,0),(2264,2056),(255,0,0),5)
cv2.rectangle(img_bgr,(300,300),(350,375),(0,255,0),3)
cv2.imwrite("1.jpg",img_bgr)
# cv2.imshow('image',img_bgr)
# cv2.waitKey(0)
# cv2.destroyAllWindows()