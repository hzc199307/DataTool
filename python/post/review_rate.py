# coding=utf-8
# by hezhichao
# 2016.12.27
# update 2017.01.04
# 计算复审率

import sys
import os

def get_lastname_of_path(path):
    return os.path.splitext(os.path.basename(path))[0]

class Review:

    def read_file_list(self,file_list):
        self.file_list = file_list

    def get_image_review_rate(self):
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
                strs = line.split("\t")
                if strs[1] == "-1":
                    continue
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

    def get_video_review_rate(self):
        self.get_video_review_rate_v1()
        self.get_video_review_rate_v2()

    def get_video_review_rate_v1(self):
        print "__________________________"
        file_count = 0
        for file in self.file_list:
            ## 针对每个file分别计算复审率
            dict_videoid_isreview = {}
            dict_label_videoid_dict = {}
            video_count = 0
            video_review_count = 0
            file_count += 1
            file_read = open(file)
            max_label_index = 0
            for line in file_read:
                strs = line.split("\t")
                if strs[1] == "-1":
                    continue
                videoid,frameid = get_lastname_of_path(strs[0]).split("_")
                ## v1
                if dict_videoid_isreview.has_key(videoid)==False:
                    dict_videoid_isreview[videoid] = (int(strs[1]) > 0)
                elif dict_videoid_isreview[videoid] == False:
                    dict_videoid_isreview[videoid] = (int(strs[1]) > 0)
                if int(strs[1]) > max_label_index:
                    max_label_index = int(strs[1])
            ## v1
            for videoid,isreview in dict_videoid_isreview.items():
                video_count += 1
                if isreview:
                    video_review_count += 1
            if file_count == 1:
                _print =  '%25s  %s' %('VideoReviewRate_v1',\
                    '  '.join(['%-8s' %('class-1~%d' %(max_label_index))]))
                print _print
            _print = '%25s  ' %get_lastname_of_path(file)
            _print += '%.7s'%(float(video_review_count*100)/video_count)+"%"
            print _print

    def get_video_review_rate_combine(self):
        print "__________________________"
        file_count = 0
        ## 针对所有file联合计算复审率
        dict_videoid_isreview = {}
        dict_label_videoid_dict = {}
        video_count = 0
        video_review_count = 0
        for file in self.file_list:
            file_count += 1
            file_read = open(file)
            for line in file_read:
                strs = line.split("\t")
                if strs[1] == "-1":
                    continue
                videoid,frameid = get_lastname_of_path(strs[0]).split("_")
                ## v1
                if dict_videoid_isreview.has_key(videoid)==False:
                    dict_videoid_isreview[videoid] = (int(strs[1]) > 0)
                elif dict_videoid_isreview[videoid] == False:
                    dict_videoid_isreview[videoid] = (int(strs[1]) > 0)
            ## v1
            for videoid,isreview in dict_videoid_isreview.items():
                video_count += 1
                if isreview:
                    video_review_count += 1
            if file_count == 1:
                _print =  '%25s  %s' %('VideoReviewRate_combine',\
                    '  '.join(['%-8s' %('class-1~End')]))
                print _print
            _print = '%25s  ' %get_lastname_of_path(file)
            if file_count == len(self.file_list):
                _print += '%.7s'%(float(video_review_count*100)/video_count)+"%"
            print _print

    def get_video_review_rate_v2(self):
        print "__________________________"
        file_count = 0
        _print_all = ""
        for file in self.file_list:
            ## 针对每个file分别计算复审率
            dict_videoid_isreview = {}
            dict_label_videoid_dict = {}
            video_count = 0
            video_review_count = 0
            file_count += 1
            file_read = open(file)
            max_label_index = 0
            for line in file_read:
                strs = line.split("\t")
                if strs[1] == "-1":
                    continue
                videoid,frameid = get_lastname_of_path(strs[0]).split("_")
                if dict_videoid_isreview.has_key(videoid)==False:
                    dict_videoid_isreview[videoid] = (int(strs[1]) > 0)
                elif dict_videoid_isreview[videoid] == False:
                    dict_videoid_isreview[videoid] = (int(strs[1]) > 0)
                ## v2
                if dict_label_videoid_dict.has_key(int(strs[1]))==False:
                    dict_label_videoid_dict[int(strs[1])] = {}
                else:
                    dict_label_videoid_dict[int(strs[1])][videoid] = True
                if int(strs[1]) > max_label_index:
                    max_label_index = int(strs[1])
            video_count = len(dict_videoid_isreview)
            if file_count == 1:
                _print =  '%25s  %s' %('VideoReviewRate_v2',\
                    '  '.join(['%-8s' %('class-%d' %c) for c in range(max_label_index+1)]) )
                print _print
            _print = '%25s  ' %get_lastname_of_path(file)
            for label in range(max_label_index+1):
                if dict_label_videoid_dict.has_key(label):
                    ratio = float(len(dict_label_videoid_dict[label]))*100/video_count
                    if ratio == 0.0:
                        _print += "0.0%      "
                    else:
                        _print += '%.7s%%  '%(ratio)
                else:
                    _print += "0.0%      "
            # _print = '%25s  %s' %(get_lastname_of_path(file),\
                    # '  '.join(['%.7s%%' %('%f' %( float( float( len(dict_label_videoid_dict[c])*100 )/video_count ) ))  for c in range(len(dict_label_videoid_dict))]) )
            print _print

if __name__ == '__main__':
    if(len(sys.argv)<2):
        print "Usage:"
        print "     python review_rate.py video/video_v1/video_v2/image/video_combine/all [classify_result_file ...]"
        exit()
    file_list = []
    for i in range(2,len(sys.argv)):
        file_list.append(sys.argv[i])
    review = Review()
    review.read_file_list(file_list)
    if sys.argv[1]=="image":
        review.get_image_review_rate()
    elif sys.argv[1]=="video":
        review.get_video_review_rate()
    elif sys.argv[1]=="video_combine":
        review.get_video_review_rate_combine()
    elif sys.argv[1]=="all":
        review.get_image_review_rate()
        print ""
        review.get_video_review_rate()
    elif sys.argv[1]=="video_v1":
        review.get_video_review_rate_v1()
    elif sys.argv[1]=="video_v2":
        review.get_video_review_rate_v2()