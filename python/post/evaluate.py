# coding=utf-8
# by hezhichao
# 2017.02.13
# update 2017.02.22
# 评价模型的Precision、Recall和ReviewRate

import sys
import os

class Tool:

	@staticmethod
	def get_lastname_of_path(path):
		return os.path.splitext(os.path.basename(path))[0]

class Evaluate:

	# 读取阈值文件
	def read_thresh_file(self,thresh_file):
		self.thresh_dict = {}
		if os.path.exists(thresh_file) == False:
			return
		thresh_file_read = open(thresh_file)
		for line in thresh_file_read:
			strs = line.strip().split()
			if len(strs)>1:
				self.thresh_dict[int(strs[0])] = float(strs[1])
			else:
				self.thresh_dict[int(strs[0])] = 0.0 #阈值默认为0.0
		thresh_file_read.close()

	# 读取多个阈值文件
	def read_thresh_file_list(self,thresh_file_list):
		self.thresh_dict_list = []
		for thresh_file in thresh_file_list:
			thresh_dict = {}
			self.thresh_dict_list.append(thresh_dict)
			if os.path.exists(thresh_file) == False:
				continue
			thresh_file_read = open(thresh_file)
			for line in thresh_file_read:
				strs = line.strip().split()
				if len(strs)>1:
					thresh_dict[int(strs[0])] = float(strs[1])
				else:
					thresh_dict[int(strs[0])] = 0.0 #阈值默认为0.0
			thresh_file_read.close()

	# 读取真值文件
	def read_groudtruth_file(self,groudtruth_file):
		self.groudtruth_dict = {}
		if os.path.exists(groudtruth_file) == False:
			return
		groudtruth_file_read = open(groudtruth_file)
		for line in groudtruth_file_read:
			strs = line.strip().split()
			self.groudtruth_dict[str(strs[0])] = int(strs[1])
		groudtruth_file_read.close()

	# 评价模型的Precision、Recall
	def process_pr(self,classify_result_file_list):
		if len(self.groudtruth_dict)>0:
		# 如果有真值表，就计算PR相关的指标并且输出
			pr_tuple_list = []
			for classify_result_file in classify_result_file_list:
				pr_tuple = PrecisionRecall.calculate_precision_recall(self.thresh_dict,self.groudtruth_dict,classify_result_file)
				pr_tuple_list.append(pr_tuple)
			PrecisionRecall.print_precision_recall(pr_tuple_list)
		else:
		# 如果真值表为空，就计算Review相关的指标并且输出
			self.process_review(classify_result_file_list,"image")

	# 评价模型的ReviewRate
	def process_review(self,classify_result_file_list,review_type="image"):
		if review_type == "image" or review_type == "all":
			review_tuple_list = []
			for classify_result_file in classify_result_file_list:
				review_tuple = Review.calculate_review(self.thresh_dict,classify_result_file)
				review_tuple_list.append(review_tuple)
			Review.print_review(review_tuple_list)
		if review_type == "video" or review_type == "all":
			review_tuple_list = []
			for classify_result_file in classify_result_file_list:
				review_tuple = Review.calculate_video_review(self.thresh_dict,classify_result_file)
				review_tuple_list.append(review_tuple)
			Review.print_review(review_tuple_list)
		if review_type == "video_combine":
			review_tuple_list = []
			review_tuple = Review.calculate_video_combine_review(self.thresh_dict_list,classify_result_file_list)
			review_tuple_list.append(review_tuple)
			Review.print_review(review_tuple_list)


class PrecisionRecall:

	# 计算PR，并且返回
	@staticmethod
	def calculate_precision_recall(thresh_dict,groudtruth_dict,classify_result_file):
		dict_correct = {}
		dict_predict_count = {}
		dict_gt_count = {}
		classify_result_file_read = open(classify_result_file)
		max_cls_index = 0
		for line in classify_result_file_read:
			strs = line.strip().split()
			NO_THRESH = ( thresh_dict.has_key(int(strs[1])) == False )
			BIGGER_THAN_THRESH = ( thresh_dict.has_key(int(strs[1])) and (float(strs[3+int(strs[1])].split(":")[1]) > thresh_dict[int(strs[1])]) )
			cls = int(strs[1])
			if (NO_THRESH or BIGGER_THAN_THRESH) == False:
				cls = 0
			gt = groudtruth_dict[strs[0]]
			if cls == gt:
				if dict_correct.has_key(cls):
					dict_correct[cls] += 1
				else:
					dict_correct[cls] = 1
			if dict_predict_count.has_key(cls):
				dict_predict_count[cls] += 1
			else:
				dict_predict_count[cls] = 1
			if dict_gt_count.has_key(gt):
				dict_gt_count[gt] += 1
			else:
				dict_gt_count[gt] = 1
			if gt > max_cls_index:
				max_cls_index = gt
			if cls > max_cls_index:
				max_cls_index = cls
		classify_result_file_read.close()
		return (classify_result_file,dict_correct,dict_predict_count,dict_gt_count,max_cls_index)

	@staticmethod
	def print_precision_recall(pr_tuple_list):
		for pr_tuple in pr_tuple_list:
			classify_result_file = pr_tuple[0]
			dict_correct = pr_tuple[1]
			dict_predict_count = pr_tuple[2]
			dict_gt_count = pr_tuple[3]
			max_cls_index = pr_tuple[4]
			print "PrecisionRecall " + classify_result_file
			print "index\tprecision\trecall\tcorrect\tpredict_count\tgt_count"
			fenzi_sum = 0
			fenmu_sum = 0
			fenzi_sum_1_end = 0
			precision_fenmu_sum_1_end = 0
			recall_fenmu_sum_1_end = 0
			for cls in range(0,max_cls_index+1):
				fenzi=0
				precision_fenmu = 0
				recall_fenmu = 0
				precision = "-"
				recall = "-"
				if dict_correct.has_key(cls):
					fenzi=dict_correct[cls]
				if dict_predict_count.has_key(cls):
					precision_fenmu=dict_predict_count[cls]
				if dict_gt_count.has_key(cls):
					recall_fenmu=dict_gt_count[cls]
				# if fenzi==0 and precision_fenmu==0 and recall_fenmu==0:
				# 	continue
				if precision_fenmu!=0:
					precision = float(fenzi)/precision_fenmu
				if recall_fenmu!=0:
					recall = float(fenzi)/recall_fenmu
				print str(cls) + "\t" + '%-10s'%('%-.5s'%str(precision)) + "\t" + '%-.5s'%str(recall) + "\t" + '%7s'%str(fenzi) + "\t" + '%13s'%str(precision_fenmu) + "\t" + '%12s'%str(recall_fenmu)
				fenzi_sum += fenzi
				fenmu_sum += precision_fenmu
				if cls != 0:
					fenzi_sum_1_end += fenzi
					precision_fenmu_sum_1_end += precision_fenmu
					recall_fenmu_sum_1_end += recall_fenmu
			print "all\t" + '%-10s'%('%-.5s'%str(float(fenzi_sum)/fenmu_sum)) + "\t" + '%-.5s'%str(float(fenzi_sum)/fenmu_sum) + "\t" + '%7s'%str(fenzi_sum) + "\t" + '%13s'%str(fenmu_sum) + "\t" + '%12s'%str(fenmu_sum)
			print "1-end\t" + '%-10s'%('%-.5s'%str(float(fenzi_sum_1_end)/precision_fenmu_sum_1_end)) + "\t" + '%-.5s'%str(float(fenzi_sum_1_end)/recall_fenmu_sum_1_end) + "\t" + '%7s'%str(fenzi_sum_1_end) + "\t" + '%13s'%str(precision_fenmu_sum_1_end) + "\t" + '%12s'%str(recall_fenmu_sum_1_end)
			print ""


class Review:

	@staticmethod
	def calculate_review(thresh_dict,classify_result_file):
		dict_cls_count = {}
		classify_result_file_read = open(classify_result_file)
		image_count = 0
		max_cls_index = 0
		for line in classify_result_file_read:
			image_count += 1
			strs = line.strip().split()
			NO_THRESH = ( thresh_dict.has_key(int(strs[1])) == False )
			BIGGER_THAN_THRESH = ( thresh_dict.has_key(int(strs[1])) and (float(strs[3+int(strs[1])].split(":")[1]) > thresh_dict[int(strs[1])]) )
			cls = int(strs[1])
			if (NO_THRESH or BIGGER_THAN_THRESH) == False:
				cls = 0
			if dict_cls_count.has_key(cls)==False:
				dict_cls_count[cls] = 0
			dict_cls_count[cls] += 1
			if cls > max_cls_index:
				max_cls_index = cls
		classify_result_file_read.close()
		# 记录 class1~End的总体复审image数目
		if dict_cls_count.has_key(0):
			dict_cls_count[-1] = image_count - dict_cls_count[0]
		title = "ImageReview\t" + classify_result_file
		return (title,dict_cls_count,image_count,max_cls_index)

	# 这是每个classify文件分开计算复审率
	@staticmethod
	def calculate_video_review(thresh_dict,classify_result_file):
		dict_cls_count = {}
		dict_cls_videoid_dict = {}
		dict_video = {}
		# dict_cls_count 和 dict_cls_videoid_dict 的 key=-1 是记录 class1~End的video复审率
		classify_result_file_read = open(classify_result_file)
		line_count = 0
		max_cls_index = 0
		for line in classify_result_file_read:
			line_count += 1
			strs = line.strip().split()
			videoid,frameid = Tool.get_lastname_of_path(strs[0]).split("_")
			dict_video[videoid] = 1
			NO_THRESH = ( thresh_dict.has_key(int(strs[1])) == False )
			BIGGER_THAN_THRESH = ( thresh_dict.has_key(int(strs[1])) and (float(strs[3+int(strs[1])].split(":")[1]) > thresh_dict[int(strs[1])]) )
			cls = int(strs[1])
			# 预测的类别有阈值的话，小于等于阈值都归为cls=0
			if (NO_THRESH or BIGGER_THAN_THRESH) == False:
				cls = 0
			if dict_cls_videoid_dict.has_key(cls)==False:
				dict_cls_videoid_dict[cls] = {}
			else:
				dict_cls_videoid_dict[cls][videoid] = True
			# 记录 class1~End的总体复审videoid
			if cls>0:
				if dict_cls_videoid_dict.has_key(-1)==False:
					dict_cls_videoid_dict[-1] = {}
				else:
					dict_cls_videoid_dict[-1][videoid] = True
			if cls > max_cls_index:
				max_cls_index = cls
		for cls,videoid_dict in dict_cls_videoid_dict.items():
			dict_cls_count[cls] = len(videoid_dict)
		video_count = len(dict_video)
		classify_result_file_read.close()
		title = "VideoReview\t" + classify_result_file
		return (title,dict_cls_count,video_count,max_cls_index)

	# 这是融合各个classify文件一起计算复审率
	@staticmethod
	def calculate_video_combine_review(thresh_dict_list,classify_result_file_list):
		# print "__________________________"
		file_count = 0
		## 针对所有file联合计算复审率
		dict_videoid_isreview = {}
		dict_label_videoid_dict = {}
		video_count = 0
		video_review_count = 0
		max_cls_index = 0
		title = "VideoCombineReview"
		for file in classify_result_file_list:
			title += "\t" + file
			thresh_dict = thresh_dict_list[file_count]
			file_count += 1
			file_read = open(file)
			for line in file_read:
				strs = line.split("\t")
				if strs[1] == "-1":
					continue
				videoid,frameid = Tool.get_lastname_of_path(strs[0]).split("_")
				## v1
				BIGGER_THAN_THRESH = ( thresh_dict.has_key(int(strs[1])) and float(strs[3+int(strs[1])].split(":")[1]) > thresh_dict[int(strs[1])] )
				NO_THRESH = (thresh_dict.has_key(int(strs[1])) == False)
				if dict_videoid_isreview.has_key(videoid)==False:
					dict_videoid_isreview[videoid] = ( (int(strs[1]) > 0) and (BIGGER_THAN_THRESH or NO_THRESH) )
				elif dict_videoid_isreview[videoid] == False:
					dict_videoid_isreview[videoid] = ( (int(strs[1]) > 0) and (BIGGER_THAN_THRESH or NO_THRESH) )
			## v1
			for videoid,isreview in dict_videoid_isreview.items():
				video_count += 1
				if isreview:
					video_review_count += 1
			# if file_count == 1:
			# 	_print =  '%25s  %s' %('VideoReviewRate_combine',\
			# 		'  '.join(['%-8s' %('class-1~End')]))
			# 	print _print
			# _print = '%25s  ' %Tool.get_lastname_of_path(file)
			# if file_count == len(classify_result_file_list):
			# 	_print += '%.7s'%(float(video_review_count*100)/video_count)+"%"
			# print _print
			file_read.close()
		dict_cls_count = {}
		dict_cls_count[-1] = video_review_count
		return (title,dict_cls_count,video_count,-1)

	@staticmethod
	def print_review(review_tuple_list):
		for review_tuple in review_tuple_list:
			title = review_tuple[0]
			dict_cls_count = review_tuple[1]
			count = review_tuple[2]
			max_cls_index = review_tuple[3]
			print title
			print "index\treview_num\treview_ratio"
			for cls in range(0,max_cls_index+1):
				if dict_cls_count.has_key(cls):
					review_num = dict_cls_count[cls]
				else:
					review_num
				review_ratio = float(review_num)/count
				print str(cls) + "\t" + '%10s'%('%-.10s'%str(review_num)) + "\t" + str(review_ratio)
			print "all\t" + '%10s'%('%-.10s'%str(count)) + "\t" + '%-.5s'%str("1.0")
			if dict_cls_count.has_key(-1):
				count_1_end = dict_cls_count[-1]#count - dict_cls_count[0]
				print "1-end\t" + '%10s'%('%-.10s'%str(count_1_end)) + "\t" + str(float(count_1_end)/count)
			print ""


if __name__ == '__main__':
	if(len(sys.argv)<4):
		print "Usage 1: 计算Precision与Recall"
		print "	python evaluate.py pr <groudtruth_file> no_thresh/<thresh_file> [<classify_result_file> ...]"
		print "	Note:"
		print "		1.阈值文件(第1列是label_index,第2列是阈值)可有可无。没有阈值的类，默认为只要分数最大即可；阈值为1.0的类，相当于把这个类过滤掉了。"
		print "		2.如果groundtruth文件存在，就计算pr指标；否则，计算复审率指标。"
		print ""
		print "Usage 2: 计算ReviewRate"
		print "	python evaluate.py review all/image/video no_thresh/<thresh_file> [<classify_result_file> ...]"
		print "	python evaluate.py review video_combine [(no_thresh/<thresh_file> <classify_result_file>) ...]"
		print "	Note:"
		print "		1.thresh_file文件和classify_result_file文件必须成对出现，最终会得到各个文件在非0类别上的复审率之和。"
		exit()
	if sys.argv[1] == "pr" or sys.argv[1] == "PR":
		groudtruth_file = sys.argv[2]
		thresh_file = sys.argv[3]
		classify_result_file_list = []
		for i in range(4,len(sys.argv)):
				classify_result_file_list.append(sys.argv[i])
		evaluate = Evaluate()
		evaluate.read_thresh_file(thresh_file)
		evaluate.read_groudtruth_file(groudtruth_file)
		evaluate.process_pr(classify_result_file_list)
	elif sys.argv[1] == "review" or sys.argv[1] == "REVIEW":
		review_type = sys.argv[2]
		evaluate = Evaluate()
		if review_type == "video_combine":
			thresh_file_list = []
			for i in range(3,len(sys.argv),2):
					thresh_file_list.append(sys.argv[i])
			classify_result_file_list = []
			for i in range(4,len(sys.argv),2):
					classify_result_file_list.append(sys.argv[i])
			evaluate.read_thresh_file_list(thresh_file_list)
		else:
			thresh_file = sys.argv[3]
			classify_result_file_list = []
			for i in range(4,len(sys.argv)):
					classify_result_file_list.append(sys.argv[i])
			evaluate.read_thresh_file(thresh_file)
		evaluate.process_review(classify_result_file_list,review_type)