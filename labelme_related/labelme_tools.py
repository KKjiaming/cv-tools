import os
import json
import cv2

def statistic_tacking(folder_path):
    '''
        这个函数用来查找folder_path中是被追踪的bbox的下xyxy以及没有被追踪的xyxy
    '''
    tracked_bbox = []
    untracked_bbox = []
    for dirpath, dirnames,  files in os.walk(folder_path):
        # print(dirpath+'\n'+dirnames+'\n'+files)
        for file in files:
            if file.endswith('.json'):
                print(os.path.join(dirpath,file))
                file_json= json.load(open(os.path.join(dirpath,file)))
                if 'shapes' in file_json.keys():
                    for detect_instance in file_json['shapes']:
                        if 'trackid' not in detect_instance.keys():
                            continue
                        if detect_instance['trackid'] != None:
                            tracked_bbox.append(detect_instance['points'])
                        else:
                            untracked_bbox.append(detect_instance['points'])
    # breakpoint()
    
    # 计算每一个bbox的面积
    tracked_area = []
    for bbox in tracked_bbox:
        [[x1,y1],[x2,y2]] = bbox
        area = (x2-x1)*(y2-y1)
        tracked_area.append(area)
    
    untracked_area = []
    for bbox in untracked_bbox:
        [[x1,y1],[x2,y2]] = bbox
        area = (x2-x1)*(y2-y1)
        untracked_area.append(area)   
        
        
    return tracked_area,untracked_area

def find_covered(result_folder_path,  ori_prefix = '/dataset/data/巡检测试集/',crop_folder = None, ori_folder = None):
    '''
        这个函数用来查找 result_folder_path 中是否存在被遮挡的目标，返回存在遮挡的原图地址
        
        result_folder_path： 待查找的文件夹路径
        ori_prefix：原图的prefix
        crop_folder：保存crop的文件夹路径
        ori_folder：保存原图的文件夹路径
        
    '''
    covered_img_path = []
    for dirpath, dirnames,  files in os.walk(result_folder_path):
    # print(dirpath+'\n'+dirnames+'\n'+files)
        for file in files:
            if file.endswith('.json'):
                # print(os.path.join(dirpath,file))
                file_json= json.load(open(os.path.join(dirpath,file)))
                if 'shapes' in file_json.keys():
                    for detect_instance in file_json['shapes']:
                        if detect_instance['is_covered']:
                            # _quchong_trackid
                            c_result_path = os.path.join(dirpath,file.replace('.json','.jpg'))
                            c_ori_path = ori_prefix+'/'.join(c_result_path.split('/')[-4:]).replace('_quchong_trackid','')
                            # c_ori_path = ori_prefix+'/'.join(c_result_path.split('/')[-4:]).replace('_quchong_trackid','')
                            print(f' The original image path is {c_ori_path} ')
                            if crop_folder != None or ori_folder != None:
                                c_ori_bgr = cv2.imread(c_ori_path)
                                if crop_folder != None:
                                    [[x1, y1], [x2, y2]] = detect_instance['points']
                                    # breakpoint()
                                    c_crop_bgr = c_ori_bgr[int(y1):int(y2), int(x1):int(x2),::1]
                                    c_crop_path = os.path.join(crop_folder,file.replace('.json',str(x1)+'.jpg'))
                                    cv2.imwrite(c_crop_path,c_crop_bgr)
                                else:
                                    c_new_path = os.path.join(ori_folder, file.replace('.json','.jpg'))
                                    cv2.imwrite(c_new_path,c_ori_bgr) 
                                    
                            # 如果不存在的话就存下来，否则继续
                            if c_ori_path not in covered_img_path:
                                covered_img_path.append(c_ori_path)
                            else:
                                continue
    # breakpoint() 
    return covered_img_path
    # d.asset_path_run('/dataset/data/巡检测试集/水泥测试集/水泥-01.04广西广昆高速',
    #                 '/dataset/result/' + save_path + '/水泥测试集/水泥-01.04广西广昆高速_quchong_trackid')     

def find_ocr(result_folder_path,  ori_prefix = '/dataset/data/巡检测试集/',crop_folder = None, ori_folder = None):
    '''
        这个函数用来查找 result_folder_path 中是否存在公里桩，返回存在公里桩的原图地址
        
        result_folder_path： 待查找的文件夹路径
        ori_prefix：原图的prefix
        crop_folder：保存crop的文件夹路径
        ori_folder：保存原图的文件夹路径
        
    '''
    covered_img_path = []
    for dirpath, dirnames,  files in os.walk(result_folder_path):
    # print(dirpath+'\n'+dirnames+'\n'+files)
        for file in files:
            if file.endswith('.json'):
                print(os.path.join(dirpath,file))
                file_json= json.load(open(os.path.join(dirpath,file)))
                if 'shapes' in file_json.keys():
                    for detect_instance in file_json['shapes']:
                        if detect_instance['ocr_name']:
                            # _quchong_trackid
                            c_result_path = os.path.join(dirpath,file.replace('.json','.jpg'))
                            breakpoint()
                            c_ori_path = ori_prefix+'/'.join(c_result_path.split('/')[:-4]).replace('_quchong_trackid','')
                            print(f' The original image path is {c_ori_path} ')
                            if crop_folder != None or ori_folder != None:
                                c_ori_bgr = cv2.imread(c_ori_path)
                                if crop_folder != None:
                                    [[x1, y1], [x2, y2]] = detect_instance['points']
                                    c_crop_bgr = c_ori_bgr[x1:x2, y1:y2,:]
                                    c_crop_path = os.path.join(crop_folder,file.replace('.json',x1+'.jpg'))
                                    cv2.imwrite(c_crop_path,c_crop_bgr)
                                else:
                                    c_new_path = os.path.join(ori_folder, file.replace('.json','.jpg'))
                                    cv2.imwrite(c_new_path,c_ori_bgr)
                                    
                            # 如果整张图没存过的话就存下来，否则继续
                            if c_ori_path not in covered_img_path:
                                covered_img_path.append(c_ori_path)
                            else:
                                continue   
    return covered_img_path
    # d.asset_path_run('/dataset/data/巡检测试集/水泥测试集/水泥-01.04广西广昆高速',
    #                 '/dataset/result/' + save_path + '/水泥测试集/水泥-01.04广西广昆高速_quchong_trackid')     


                           
if __name__ == '__main__':
    folder_path = '/dataset/result/asset_detect_v0.6.0/水泥测试集'
    # tracked_area,untracked_area = statistic_tacking(folder_path)
    find_covered(folder_path,crop_folder ='/home/smartmore/workspace/jiamingyue/test_out/遮挡2/')
    breakpoint()
    