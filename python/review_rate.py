# coding=utf-8
# by hezhichao
# 2016.12.27
# 计算复审率

import sys
import os

def get_lastname_of_path(path):
    return os.path.splitext(os.path.basename(path))[0]

class Review:

    def read_file_list(self,file_list):
        self.file_list = file_list

    def get_image_review_rate(self):
        file_count = 0
        for file in self.file_list:
            ## 针对每个file分别计算复审率
            dict = {}
            line_count = 0
            file_count += 1
            file_read = open(file)
            for line in file_read:
                line_count += 1
                strs = line.split("\t")
                if dict.has_key(int(strs[1])):
                    dict[int(strs[1])] += 1
                else:
                    dict[int(strs[1])] = 1
            if file_count == 1:
                _print =  '%25s  %s' %('ImageReviewRate',\
                    '  '.join(['%9s' %('class-%d' %c) for c in range(len(dict))]))
                print _print
            _print = '%25s  ' %get_lastname_of_path(file)
            for key,value in dict.items():
                _print += '%8f'%(float(value)*100/line_count)+"%  "
            print _print

    def get_video_review_rate(self):
        file_count = 0
        for file in self.file_list:
            ## 针对每个file分别计算复审率
            dict_videoid_isreview = {}
            video_count = 0
            video_review_count = 0
            file_count += 1
            file_read = open(file)
            max_label_index = 0
            for line in file_read:
                strs = line.split("\t")
                videoid,frameid = get_lastname_of_path(strs[0]).split("_")
                if dict_videoid_isreview.has_key(videoid)==False:
                    dict_videoid_isreview[videoid] = (int(strs[1]) > 0)
                elif dict_videoid_isreview[videoid] == False:
                    dict_videoid_isreview[videoid] = (int(strs[1]) > 0)
                if int(strs[1]) > max_label_index:
                    max_label_index = int(strs[1])
            for videoid,isreview in dict_videoid_isreview.items():
                video_count += 1
                if isreview:
                    video_review_count += 1
            if file_count == 1:
                _print =  '%25s  %s' %('VideoReviewRate',\
                    '  '.join(['%9s' %('class-1~%d' %(max_label_index))]))
                print _print
            _print = '%25s  ' %get_lastname_of_path(file)
            _print += '%8f'%(float(video_review_count)*100/video_count)+"%"
            print _print

if __name__ == '__main__':
    if(len(sys.argv)<2):
        print "python review_rate.py video/image/all [classify_result_file ...]"
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
    elif sys.argv[1]=="all":
        review.get_image_review_rate()
        print "\n"
        review.get_video_review_rate()