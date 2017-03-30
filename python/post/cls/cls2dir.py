# coding=utf-8
# by hezhichao
# 2017.01.04
# update 2017.01.04
# 根据分类结果文件把图片移动到文件夹里面

import os
import sys


class Cls2Dir:
    @staticmethod
    def read_file_list(classify_result_file, dst_dir_path):
        file_read = open(classify_result_file)
        if dst_dir_path != '/':
            dst_dir_path += "/"
        if os.path.exists(dst_dir_path) == False:
            os.makedirs(dst_dir_path)
        for line in file_read:
            strs = line.strip().split()
            if len(strs)>1:
                if strs[1] == "-1":
                    continue
                if os.path.exists(dst_dir_path + strs[1]) == False:
                    os.makedirs(dst_dir_path + strs[1])
                os.system('cp ' + strs[0] + " " + dst_dir_path + strs[1])
            else:
                os.system('cp ' + strs[0] + " " + dst_dir_path)


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print "Usage:"
        print "     python cls2dir.py classify_result_file dst_dir_path"
        exit()
    Cls2Dir.read_file_list(str(sys.argv[1]), str(sys.argv[2]))