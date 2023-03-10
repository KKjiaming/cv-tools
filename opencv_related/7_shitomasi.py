import numpy as np
import cv2


def getkpoints(imag, input1):
    mask1 = np.zeros_like(input1)
    x = 0
    y = 0
    w1, h1 = input1.shape
    input1 = input1[0:w1, 200:h1]

    try:
        w, h = imag.shape
    except:
        return None

    mask1[y:y + h, x:x + w] = 255          # 整张图片像素
    keypoints = []
    kp = cv2.goodFeaturesToTrack(input1, 200, 0.001, 3,useHarrisDetector=True,k=0.06)
    print(kp)
    # breakpoint()
    if kp is not None and len(kp) > 0:
        for x, y in np.float32(kp).reshape(-1, 2):
            keypoints.append((x, y))
    return keypoints

def process(image):
    grey1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grey = cv2.equalizeHist(grey1)
    keypoints = getkpoints(grey, grey1)

    if keypoints is not None and len(keypoints) > 0:
        for x, y in keypoints:
            cv2.circle(image, (int(x + 200), y), 3, (255, 255, 0))
    return image

if __name__ == '__main__':
    img_path = r"crop_img\2232.02365_2022-12-09_10-23-12-985.jpg"
    img_bgr = cv2.imread(img_path)
    print(f'shape of the img is {img_bgr.shape[0]} and {img_bgr.shape[1]}')
    img_point = process(img_bgr)
    cv2.imshow('img_point',img_point)
    
    # cap = cv2.VideoCapture("IMG_1521.mp4")
    # while (cap.isOpened()):
    
    #     ret, frame = cap.read()
    #     frame = process(frame)
    #     cv2.imshow('frame', frame)
    #     if cv2.waitKey(27) & 0xFF == ord('q'):
    #         break
    # cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
