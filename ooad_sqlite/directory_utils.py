from os import listdir, mkdir
from os.path import isfile
from os.path import splitext
import os.path
import os
import shutil


class Directory:
    cur_path = './'
    __dir_list = []

    def __init__(self, cur_path):
        self.cur_path = cur_path
        self.create_folder('')
        self.__dir_list = listdir(self.cur_path)

    def set_cur_path(self, cur_path):
        self.cur_path = cur_path

    def get_tex_files_list(self):
        self.__dir_list = listdir(self.cur_path)
        result = []
        for dir in self.__dir_list:
            # print(dir)
            # if isfile(dir):
            post_fix = splitext(dir)[-1]
            if post_fix == '.tex':
                result.append(dir.split('/')[-1])
        return result

    def get_files_and_folders(self):
        self.__dir_list = listdir(self.cur_path)
        result = []
        for dir in self.__dir_list:
            if isfile(self.cur_path + dir):
                result.append((True, dir))
            else:
                result.append((False, dir))
        return result

    def create_folder(self, folder_name):
        if not os.path.exists(self.cur_path + folder_name):
            print('create a folder!')
            mkdir(self.cur_path + folder_name)

    def copy_folder(self, folder_name):
        src_path = self.cur_path + folder_name
        tgt_path = self.cur_path + folder_name + '_copy'
        assert os.path.exists(src_path)
        assert not os.path.exists(tgt_path)
        shutil.copytree(src_path, tgt_path)

    def copy_file(self, file_name):
        src_path = self.cur_path + file_name
        tgt_path = self.cur_path + file_name + '_copy'
        assert os.path.exists(src_path)
        assert not os.path.exists(tgt_path)
        shutil.copy(src_path, tgt_path)

    def delete_folder(self, folder_name):
        total_path = self.cur_path + folder_name
        if os.path.exists(total_path):
            os.removedirs(total_path);
            print('delete a folder')
        else:
            print('folder not exist')
        pass

    def delete_file(self, file_name):
        total_path = self.cur_path + file_name
        files_and_folders = self.get_files_and_folders()
        is_file, names = zip(*files_and_folders)
        # assert file_name in names
        assert os.path.exists(total_path)
        for is_file, name in files_and_folders:
            if name == file_name:
                assert is_file
        os.remove(total_path)

    def rename_ff(self, old_name, new_name):
        # 目前文件夹和文件不可同名, 即如果文件夹为name, 文件不可重命名为name
        '''
        Both file and folder can be rename
        :return:
        '''
        old_path = self.cur_path + old_name
        new_path = self.cur_path + new_name
        assert os.path.exists(old_path)
        assert not os.path.exists(new_path)
        os.rename(old_path, new_path)
        print('rename!')
