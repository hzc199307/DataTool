# coding=utf-8
# by hezhichao
# 2017.01.12
# update 2017.01.12
# 计算识别率

import sys
import os

def get_lastname_of_path(path):
    return os.path.splitext(os.path.basename(path))[0]

class Recog:

    def read_file_list(self,file_list):
        self.file_list = file_list

    def get_image_recog(self,threshold,isNUM = False):
        print "__________________________"
        file_count = 0
        for file in self.file_list:
            ## 针对每个file分别计算复审率
            # images_count_perlabel = np.zeros((class_num),dtype=np.int32)
            dict = {}
            line_count = 0
            file_count += 1
            file_read = open(file)
            max_label_index = 0
            for line in file_read:
                line_count += 1
                strs = line.strip().split()
                if strs[1] == "-1":
                    continue
                elif strs[1] == "0":
                	max_score = float(strs[4].split(":")[1])
                	max_score_index = 1
                	for i in range(5,len(strs)):
                		if float(strs[i].split(":")[1]) > max_score:
                			max_score = float(strs[i].split(":")[1])
                			max_score_index = i-3
                	if max_score > threshold:
                		strs[1] = str(max_score_index)
                if dict.has_key(int(strs[1])):
                    dict[int(strs[1])] += 1
                else:
                    dict[int(strs[1])] = 1
                if int(strs[1]) > max_label_index:
                    max_label_index = int(strs[1])
            if file_count == 1:
                _print =  '%25s  %s' %('ImageReviewRate',\
                    '  '.join(['%-8s' %('class-%d' %c) for c in range(max_label_index+1)]))
                print _print
            _print = '%25s  ' %get_lastname_of_path(file)
            if isNUM:
                for label in range(max_label_index+1):
                    if dict.has_key(label):
                        num = int(dict[label])
                        _print += '%-7d   '%(num)
                    else:
                        _print += "0         "
                print _print
            else:
                for label in range(max_label_index+1):
                    if dict.has_key(label):
                        ratio = float(dict[label])*100/line_count
                        if ratio == 0.0:
                            _print += "0.0%      "
                        else:
                            _print += '%.7s%%  '%(ratio)
                    else:
                        _print += "0.0%      "
                print _print

if __name__ == '__main__':
    if(len(sys.argv)<5):
        print "Usage:"
        print "     python recog_rate.py ratio/num video/image/all threshold [classify_result_file ...]"
        exit()
    file_list = []
    isNUM = False
    if sys.argv[1]=="num": 
        isNUM = True
    threshold = float(sys.argv[3])
    for i in range(4,len(sys.argv)):
        file_list.append(sys.argv[i])
    recog = Recog()
    recog.read_file_list(file_list)
    if sys.argv[2]=="image":
        recog.get_image_recog(threshold,isNUM)