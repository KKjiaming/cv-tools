import os
from shutil import copy, rmtree
import random

class CreatDataset():
    """
    ori_folder: all images path
    rate: "train: val :test"
    Formate:
    --root
        --ori_folder
            --class 1
            ... ...
            
            --train
                --class 1
                ... ...
            --val
                --class 1
                ... ...
            --test
                --class 1
                ... ...
    """
    def __init__(self, ori_folder, rate='8:2') -> None:
        self.ori_folder = ori_folder
        
        # 获取主目录下所有文件夹的类别信息
        self.data_class = [cla for cla in os.listdir(self.ori_folder)
                        if os.path.isdir(os.path.join(self.ori_folder, cla))]
        
        self.resolve_rate(rate)
    
    def resolve_rate(self,rate:str):
        '''
            解析字符串：
                train: test = 8:2
        '''
        rates = rate.split(':') 
        self.train_rate = int(rates[0])
        self.val_rate = int(rates[1])
        if len(rates) == 3:
            self.test_rate = int(rates[2])
        else:
            self.test_rate = 0

    def mk_folder(self, mode: str):
        # 建立保存训练集,的文件夹
        tvt_root = os.path.join(self.ori_folder, mode)
        if os.path.exists(tvt_root):
            # 如果文件夹存在，则先删除原文件夹及其所包含的所有文件，并重新创建新的文件夹
            rmtree(tvt_root)
        os.makedirs(tvt_root)
        for cla in self.data_class:
            # 建立每个类别对应的文件夹
            cla_path = os.path.join(tvt_root,cla)
            if os.path.exists(cla_path):
                rmtree(cla_path)
            os.makedirs(cla_path)
            
    def split_dataset(self ):
        # 保证随机可复现
        random.seed(0)
        # 指向存放分类图像数据的主目录
        assert os.path.exists(self.ori_folder), "path '{}' does not exist.".format(self.ori_folder)
        
        # train/val/test 文件创建
        train_root = self.mk_folder("train")
        val_root = self.mk_folder("val")
        if self.test_rate != 0:
            test_root = self.mk_folder("test")
        
        # 根据数据集类别进行划分
        for cla in self.data_class:
            cla_path = os.path.join(self.ori_folder, cla)
            images = os.listdir(cla_path)
            num = len(images)
    
            # 随机采样验证集的索引
            eval_index = random.sample(images, k=int(num*self.eval_rate))
            test_index = random.sample(images, k=int(num*self.test_rate))
            
            for index, image in enumerate(images):
                if image in eval_index:
                    # 将分配至验证集中的文件复制到相应目录
                    image_path = os.path.join(cla_path, image)
                    new_path = os.path.join(val_root, cla)
                    copy(image_path, new_path)  # copy(原始路径，新的路径)
                elif image in test_index:
                    # 将分配至测试集中的文件复制到相应目录
                    image_path = os.path.join(cla_path, image)
                    new_path = os.path.join(test_root, cla)
                    copy(image_path, new_path)
                else:
                    # 将分配至训练集中的文件复制到相应目录
                    image_path = os.path.join(cla_path, image)
                    new_path = os.path.join(train_root, cla)
                    copy(image_path, new_path)
                    
                print("\r[{}] processing [{}/{}]".format(cla, index+1, num), end="")  # processing bar
            print()
    
        print("processing done!")
 