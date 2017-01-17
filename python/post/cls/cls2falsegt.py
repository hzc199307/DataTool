# coding=utf-8
# by hezhichao
# 2017.01.05
# update 2017.01.05
# 根据分类结果文件和gt文件，找出分错的样本

import os
import sys


class Cls2FalseGT:

    @staticmethod
    def read_file_list(classify_result_file, gt_file,output_hardcase_gt_file,output_hardcase_md5_gt_file=None):
        # 先预存储md5和label
        dict_case_gt_md5 = {}
        gt_file_read = open(gt_file)
        for line in gt_file_read:
            strs = line.strip().split()
            dict_case_gt_md5[strs[0]]={}
            dict_case_gt_md5[strs[0]]["gt"] = int(strs[1])
            dict_case_gt_md5[strs[0]]["md5"] = strs[2]
        gt_file_read.close()
        # 读取cls结果文件，然后再把错误的样本存储
        classify_result_file_read = open(classify_result_file)
        output_hardcase_gt_file_write = open(output_hardcase_gt_file,"w+")
        if output_hardcase_md5_gt_file!=None:
            output_hardcase_md5_gt_file_write = open(output_hardcase_md5_gt_file,"w+")
        for line in classify_result_file_read:
            strs = line.strip().split()
            if strs[1] == "-1":
                continue
            if dict_case_gt_md5[strs[0]]["gt"] != int(strs[1]):
                output_hardcase_gt_file_write.write(strs[0]+" "+str(dict_case_gt_md5[strs[0]]["gt"])+"\n")
                if output_hardcase_md5_gt_file!=None:
                    output_hardcase_md5_gt_file_write.write(dict_case_gt_md5[strs[0]]["md5"]+" "+str(dict_case_gt_md5[strs[0]]["gt"])+"\n")
        classify_result_file_read.close()
        output_hardcase_gt_file_write.close()
        output_hardcase_md5_gt_file_write.close()
            
if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print "Usage:"
        print "     1:  python cls2falsegt.py classify_result_file gt_file output_hardcase_gt_file"
        print "     2:  python cls2falsegt.py classify_result_file gtmd5_file output_hardcase_gt_file output_hardcase_md5_gt_file"
        print "\nExample:"
        print "python cls2falsegt.py /data/greendam/model_training/greendam_scene_v2/data/scene_v2_1/result/scene_v2_1_train.scene_v2_1_0_16k.cls /data/greendam/model_training/greendam_scene_v2/data/scene_v2_1/list/scene_v2_1_train.gtmd5 /data/greendam/model_training/greendam_scene_v2/data/scene_v2_1/list/hardcases.scene_v2_1_train.scene_v2_1_0_16k.gt /data/greendam/model_training/greendam_scene_v2/data/scene_v2_1/list/hardcases.scene_v2_1_train_md5.scene_v2_1_0_16k.gt"
        exit()
    if (len(sys.argv) == 4):
        Cls2FalseGT.read_file_list(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
    elif (len(sys.argv) == 5):
        Cls2FalseGT.read_file_list(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))