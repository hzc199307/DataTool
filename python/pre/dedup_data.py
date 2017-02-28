# coding=utf-8
# by hezhichao
# 2017.02.10
# update 2017.02.10
# 去除重复的行

import sys
import os

def DEDUP_DATA(type_,input_file_paths_list,output_file_path):
    DedupData.process(input_file_paths_list,output_file_path,type_)

class Tool:

    @staticmethod
    def get_lastname_of_path(path):
        return os.path.splitext(os.path.basename(path))[0]

class DedupData:

    @staticmethod
    def process(input_file_paths_list,output_file_path,type):
        if type=="list" or type=="lst":
            DedupData.process_list(input_file_paths_list,output_file_path)
        elif type=="path_gt":
            DedupData.process_path_gt(input_file_paths_list,output_file_path)
        elif type=="filename_gt":
            DedupData.process_filename_gt(input_file_paths_list,output_file_path)

    @staticmethod
    def process_list(input_file_paths_list,output_file_path):
        dict_lines = {}
        for input_file in input_file_paths_list:
            input_file_read = open(input_file)
            for line in input_file_read:
                dict_lines[line.strip()] = ""
            input_file_read.close()
        output_file_path_write = open(output_file_path,"w+")
        for line in dict_lines.keys():
            output_file_path_write.write(line + "\n")
        output_file_path_write.close()

    @staticmethod
    def process_path_gt(input_file_paths_list,output_file_path):
        dict_lines = {}
        for input_file in input_file_paths_list:
            input_file_read = open(input_file)
            for line in input_file_read:
                strs = line.strip().split()
                if dict_lines.has_key(strs[0]) == False:
                    dict_lines[strs[0]] = strs[1] # 只保留第一次出现的时候的label
                #elif dict_lines[strs[0]] != strs[1]:
                    #print strs[0] + " " + dict_lines[strs[0]]  + " " +strs[1]
                    #dict_lines[strs[0]] = ""
            input_file_read.close()
        output_file_path_write = open(output_file_path,"w+")
        for path,gt in dict_lines.items():
            if gt != "":
                output_file_path_write.write(path + " " + gt + "\n")
        output_file_path_write.close()

    @staticmethod
    def process_filename_gt(input_file_paths_list,output_file_path):
        dict_lines = {}
        for input_file in input_file_paths_list:
            input_file_read = open(input_file)
            for line in input_file_read:
                strs = line.strip().split()
                filename = Tool.get_lastname_of_path(strs[0])
                if dict_lines.has_key(filename) == False:
                    dict_lines[filename] = {}
                    dict_lines[filename]["path"] = strs[0]
                    dict_lines[filename]["gt"] = strs[1] # 只保留第一次出现的时候的label
                #elif dict_lines[strs[0]] != strs[1]:
                    #print strs[0] + " " + dict_lines[strs[0]]  + " " +strs[1]
                    #dict_lines[strs[0]] = ""
            input_file_read.close()
        output_file_path_write = open(output_file_path,"w+")
        for filename,record in dict_lines.items():
            if record["gt"] != "":
                output_file_path_write.write(record["path"] + " " + record["gt"] + "\n")
        output_file_path_write.close()

if __name__ == '__main__':
    if(len(sys.argv)<3):
        print "Usage:"
        print "     python dedup_data.py list(lst)/path_gt/filename_gt [input_file_paths ...] [output_file_path]"
        exit()
    type_ = sys.argv[1]
    input_file_paths_list = []
    for i in range(2,len(sys.argv)-1):
        input_file_paths_list.append(sys.argv[i])
    output_file_path = sys.argv[len(sys.argv)-1]
    DedupData.process(input_file_paths_list,output_file_path,type_)