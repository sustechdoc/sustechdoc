from os import listdir,mkdir
from os.path import isfile
from os.path import splitext
import os.path
import os
# TODO 改变工作目录到指定目录
class Directory:
    cur_path = './'
    __dir_list = []

    def __init__(self, cur_path):
        self.cur_path = cur_path
        self.create_folder('')
        self. __dir_list = listdir(self.cur_path)

    def get_tex_files_list(self):
        result = []
        for dir in self.__dir_list:
            # print(dir)
            # if isfile(dir):
            post_fix = splitext(dir)[-1]
            if post_fix == '.tex':
                result.append(dir.split('/')[-1])
        return result

    def get_files_and_folders(self):
        result=[]
        for dir in self.__dir_list:
            if isfile(self.cur_path+dir):
                result.append((True,dir))
            else:
                result.append((False,dir))
        return result

    def create_folder(self, folder_name):
        if not os.path.exists(self.cur_path+folder_name):
            print('create a folder!')
            mkdir(self.cur_path+folder_name)
