# coding=utf-8
# by hezhichao
# 2016.12.27
# update 2017.01.04
# 计算复审率

import sys
import os

def get_lastname_of_path(path):
    return os.path.splitext(os.path.basename(path))[0]

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


class Review:

    def read_thresh_file(self,thresh_file):
        self.thresh_dict = {}
        if os.path.exists(thresh_file) == False:
            return
        thresh_file_read = open(thresh_file)
        for line in thresh_file_read:
            strs = line.strip().split()
            self.thresh_dict[int(strs[0])] = float(strs[1])

    def read_file_list(self,file_list):
        self.file_list = file_list

    def get_image_review_rate(self,isNUM = False):
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

    def get_image_review_rate_with_threshold(self,isNUM = False):
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
                if dict.has_key(int(strs[1])) == False:
                    dict[int(strs[1])] = 0
                # 必须大于阈值 或者没有阈值，才+1
                BIGGER_THAN_THRESH = ( self.thresh_dict.has_key(int(strs[1])) and float(strs[3+int(strs[1])].split(":")[1]) > self.thresh_dict[int(strs[1])] )
                NO_THRESH = (self.thresh_dict.has_key(int(strs[1])) == False)
                if NO_THRESH or BIGGER_THAN_THRESH:
                    dict[int(strs[1])] += 1
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

    def get_video_review_rate(self,isNUM = False):
        self.get_video_review_rate_v1()
        self.get_video_review_rate_v2()

    def get_video_review_rate_v1(self,isNUM = False):
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

    def get_video_review_rate_combine(self,isNUM = False):
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

    def get_video_review_rate_v2(self,isNUM = False):
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

    @staticmethod
    def review(label,score,thresh):
        for case in switch(label):
            if case(0):
                return score < thresh[label]
                break
            if case(): # 默认
                return score >= thresh[label]
                break

    def get_video_review_rate_v3(self,isNUM = False):
        thresh = [0,0.85,0.6,0.9,0.85,0.8,0.85,0.75,0.7,0.85,0.85,0.55,0.5,0.6,0.5,0.6,0.7,0.93,0.7,0.86,0.6,0.91,0.55,0.55,0.995,0.92]
        class_array = []
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
                    dict_videoid_isreview[videoid] = Review.review(int(strs[1]),float( strs[int(strs[1])+3].split(":")[1] ),thresh)
                elif dict_videoid_isreview[videoid] == False:
                    dict_videoid_isreview[videoid] = Review.review(int(strs[1]),float( strs[int(strs[1])+3].split(":")[1] ),thresh)
                if int(strs[1]) > max_label_index:
                    max_label_index = int(strs[1])
            ## v1
            for videoid,isreview in dict_videoid_isreview.items():
                video_count += 1
                if isreview:
                    video_review_count += 1
            if file_count == 1:
                _print =  '%25s  %s' %('VideoReviewRate_v1',\
                    '  '.join(['%-8s' %('class-1~%d 阈值' %(max_label_index))]))
                _print += str(thresh)
                print _print
            _print = '%25s  ' %get_lastname_of_path(file)
            _print += '%.7s'%(float(video_review_count*100)/video_count)+"%"
            print _print

if __name__ == '__main__':
    if(len(sys.argv)<4):
        print "Usage:"
        print "     python review_rate.py ratio/num video/video_v1/video_v2/image/video_combine/all [classify_result_file ...]"
        print "     python review_rate.py ratio/num image_thresh/video_thresh/all_thresh [threshold_file] [classify_result_file ...]"
        exit()
    file_list = []
    isNUM = False
    if sys.argv[1]=="num": 
        isNUM = True
    if sys.argv[2].find("thresh")!=-1:
        for i in range(4,len(sys.argv)):
            file_list.append(sys.argv[i])
    else:
        for i in range(3,len(sys.argv)):
            file_list.append(sys.argv[i])
    review = Review()
    review.read_file_list(file_list)
    if sys.argv[2]=="image":
        review.get_image_review_rate(isNUM)
    elif sys.argv[2]=="video":
        review.get_video_review_rate()
    elif sys.argv[2]=="video_combine":
        review.get_video_review_rate_combine()
    elif sys.argv[2]=="all":
        review.get_image_review_rate()
        print ""
        review.get_video_review_rate()
    elif sys.argv[2]=="video_v1":
        review.get_video_review_rate_v1()
    elif sys.argv[2]=="video_v2":
        review.get_video_review_rate_v2()
    elif sys.argv[2]=="video_v3":
        review.get_video_review_rate_v3()
    elif sys.argv[2]=="image_thresh":
        threshold_file = sys.argv[3]
        review.read_thresh_file(threshold_file)
        review.get_image_review_rate_with_threshold(isNUM)