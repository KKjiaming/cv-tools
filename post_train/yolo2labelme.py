import os
import json
import cv2
import base64
root_folder = r'D:\yolov5_6.2_asset\glz_zs2\valid'

img_folder = os.path.join(root_folder,'image')
txt_folder = os.path.join(root_folder,'txt')
json_folder = os.path.join(root_folder,'json')

num_name = {'0':'longmenjia','1':'dianziqingbaoban','2':'jiaotongxinhaodeng','3':'jinggai','4':'jiaotongbiaozhi','5': 'sanjiaobiaozhi','6':'yuanbiaozhi','7':'gonglizhuang'}

if not os.path.exists(json_folder):
    os.makedirs(json_folder)
    
version = '3.16.7'
flags = {}
lineColor = [0, 255, 0, 128]
fillColor = [255, 0, 0, 128]
for file in os.listdir(img_folder):
    if 'jpg' in file:
        dic = {}
        dic['version'] = version
        dic['flags'] = flags
        dic['shapes'] = []  
        
        img = cv2.imread(os.path.join(img_folder,file))
        
        # img = cv2.imread('{}/{}'.format(img_folder,file))
        # import pdb;pdb.set_trace()
        if img is None:
            continue
        imageHeight,imageWidth,_ = img.shape
        if os.path.exists(os.path.join(txt_folder,file.split('.')[0])+'.txt'):
            with open(os.path.join(txt_folder,file.split('.')[0])+'.txt') as f:
            #with open('txt_folder/{}.txt'.format(file.split('.')[0])) as f:
                datas = f.readlines()
                for data in datas:
                    shape = {}
                    label = num_name[data[0]]
                    shape['label'] = label
                    shape['line_color'] = None
                    shape['fill_color'] = None
                    data = data.strip().split(' ')
                    x = float(data[1]) * imageWidth
                    y = float(data[2]) * imageHeight
                    w = float(data[3]) * imageWidth
                    h = float(data[4]) * imageHeight
                    x1 = x - w / 2
                    y1 = y - h / 2
                    x2 = x1 + w
                    y2 = y1 + h
                    shape['points'] = [[x1,y1],[x2,y2]]
                    shape['shape_type'] = 'rectangle'
                    shape['flags'] = {}
                    dic['shapes'].append(shape)
            dic['lineColor'] = lineColor
            dic['fillColor'] = fillColor
            dic['imagePath'] = file
            #'{}/{}'.format(img_folder,file)
            # dic['imageData'] = base64.b64encode(open(os.path.join(img_folder,file),"rb").read()).decode('utf-8')
            dic['imageData'] = ''
            dic['imageHeight'] = imageHeight
            dic['imageWidth'] = imageWidth
            fw = open(os.path.join(json_folder,file.split('.')[0])+".json",'w')
            json.dump(dic,fw)
            fw.close()
        # import pdb;pdb.set_trace()