import cv2
import numpy as np

img_path = r"D:\jiqun\asset_tracking\quchong\2023-2-21_new_new\2023-02-21-15-15-28\3665_2023-02-21_15-15-28-774.jpg"
img_bgr = cv2.imread(img_path)
# breakpoint()
cv2.line(img_bgr,(200,0),(200,2056),(255,0,0),5)
cv2.line(img_bgr,(2264,0),(2264,2056),(255,0,0),5)
cv2.rectangle(img_bgr,(300,300),(330,330),(0,255,0),3)
cv2.imwrite("1.jpg",img_bgr)
cv2.imshow('image',img_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()