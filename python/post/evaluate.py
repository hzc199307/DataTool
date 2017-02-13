# coding=utf-8
# by hezhichao
# 2017.02.13
# update 2017.02.13
# 评价模型

import sys
import os

class Evaluate:

	def read_thresh_file(self,thresh_file):
		self.thresh_dict = {}
		if os.path.exists(thresh_file) == False:
			return
		thresh_file_read = open(thresh_file)
		for line in thresh_file_read:
			strs = line.strip().split()
			self.thresh_dict[int(strs[0])] = float(strs[1])

	def read_groudtruth_file(self,groudtruth_file):
		self.groudtruth_dict = {}
		if os.path.exists(groudtruth_file) == False:
			return
		groudtruth_file_read = open(groudtruth_file)
		for line in groudtruth_file_read:
			strs = line.strip().split()
			self.groudtruth_dict[str(strs[0])] = int(strs[1])

	def process(self,classify_result_file_list):
		# 如果有真值表，就计算PR相关的指标并且输出
		if len(self.groudtruth_dict)==0:
			review_tuple_list = []
			for classify_result_file in classify_result_file_list:
				review_tuple = Review.calculate_review(self.thresh_dict,classify_result_file)
				review_tuple_list.append(review_tuple)
			Review.print_review(review_tuple_list)
		# 如果没有真值表，就计算Review相关的指标并且输出
		else:
			pr_tuple_list = []
			for classify_result_file in classify_result_file_list:
				pr_tuple = PrecisionRecall.calculate_precision_recall(self.thresh_dict,self.groudtruth_dict,classify_result_file)
				pr_tuple_list.append(pr_tuple)
			PrecisionRecall.print_precision_recall(pr_tuple_list)

class PrecisionRecall:

	@staticmethod
	def calculate_precision_recall(thresh_dict,groudtruth_dict,classify_result_file):
		dict_fenzi = {}
		dict_precision_fenmu = {}
		dict_recall_fenmu = {}
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
				if dict_fenzi.has_key(cls):
					dict_fenzi[cls] += 1
				else:
					dict_fenzi[cls] = 1
			if dict_precision_fenmu.has_key(cls):
				dict_precision_fenmu[cls] += 1
			else:
				dict_precision_fenmu[cls] = 1
			if dict_recall_fenmu.has_key(gt):
				dict_recall_fenmu[gt] += 1
			else:
				dict_recall_fenmu[gt] = 1
			if gt > max_cls_index:
				max_cls_index = gt
			if cls > max_cls_index:
				max_cls_index = cls
		return (classify_result_file,dict_fenzi,dict_precision_fenmu,dict_recall_fenmu,max_cls_index)

	@staticmethod
	def print_precision_recall(pr_tuple_list):
		for pr_tuple in pr_tuple_list:
			classify_result_file = pr_tuple[0]
			dict_fenzi = pr_tuple[1]
			dict_precision_fenmu = pr_tuple[2]
			dict_recall_fenmu = pr_tuple[3]
			max_cls_index = pr_tuple[4]
			print "# " + classify_result_file
			print "index\tprecision\trecall\t  fenzi\tprecision_fenmu\trecall_fenmu"
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
				if dict_fenzi.has_key(cls):
					fenzi=dict_fenzi[cls]
				if dict_precision_fenmu.has_key(cls):
					precision_fenmu=dict_precision_fenmu[cls]
				if dict_recall_fenmu.has_key(cls):
					recall_fenmu=dict_recall_fenmu[cls]
				if fenzi==0 and precision_fenmu==0 and recall_fenmu==0:
					continue
				if precision_fenmu!=0:
					precision = float(fenzi)/precision_fenmu
				if recall_fenmu!=0:
					recall = float(fenzi)/recall_fenmu
				print str(cls) + "\t" + '%-10s'%('%-.5s'%str(precision)) + "\t" + '%-.5s'%str(recall) + "\t" + '%7s'%str(fenzi) + "\t" + '%15s'%str(precision_fenmu) + "\t" + '%12s'%str(recall_fenmu)
				fenzi_sum += fenzi
				fenmu_sum += precision_fenmu
				if cls != 0:
					fenzi_sum_1_end += fenzi
					precision_fenmu_sum_1_end += precision_fenmu
					recall_fenmu_sum_1_end += recall_fenmu
			print "all\t" + '%-10s'%('%-.5s'%str(float(fenzi_sum)/fenmu_sum)) + "\t" + '%-.5s'%str(float(fenzi_sum)/fenmu_sum) + "\t" + '%7s'%str(fenzi_sum) + "\t" + '%15s'%str(fenmu_sum) + "\t" + '%12s'%str(fenmu_sum)
			print "0-end\t" + '%-10s'%('%-.5s'%str(float(fenzi_sum_1_end)/precision_fenmu_sum_1_end)) + "\t" + '%-.5s'%str(float(fenzi_sum_1_end)/recall_fenmu_sum_1_end) + "\t" + '%7s'%str(fenzi_sum_1_end) + "\t" + '%15s'%str(precision_fenmu_sum_1_end) + "\t" + '%12s'%str(recall_fenmu_sum_1_end)
			print ""

class Review:

	@staticmethod
	def calculate_review(thresh_dict,classify_result_file):
		dict_cls_count = {}
		classify_result_file_read = open(classify_result_file)
		line_count = 0
		for line in classify_result_file_read:
			line_count += 1
			strs = line.strip().split()
			NO_THRESH = ( thresh_dict.has_key(int(strs[1])) == False )
			BIGGER_THAN_THRESH = ( thresh_dict.has_key(int(strs[1])) and (float(strs[3+int(strs[1])].split(":")[1]) > thresh_dict[int(strs[1])]) )
			cls = int(strs[1])
			if (NO_THRESH or BIGGER_THAN_THRESH) == False:
				cls = 0
			if dict_cls_count.has_key(cls)==False:
				dict_cls_count[cls] = 0
			dict_cls_count[cls] += 1
		return (classify_result_file,dict_cls_count,line_count)

	@staticmethod
	def print_review(review_tuple_list):
		for review_tuple in review_tuple_list:
			classify_result_file = review_tuple[0]
			dict_cls_count = review_tuple[1]
			line_count = review_tuple[2]
			if dict_cls_count.has_key(0):
				line_count_0_end = line_count - dict_cls_count[0]
			print "# " + classify_result_file
			print "index\treview_num\treview_ratio"
			for cls,review_num in dict_cls_count.items():
				review_ratio = float(review_num)/line_count
				print str(cls) + "\t" + '%10s'%('%-.10s'%str(review_num)) + "\t" + str(review_ratio)
			print "all\t" + '%10s'%('%-.10s'%str(line_count)) + "\t" + '%-.5s'%str("1.0")
			print "0-end\t" + '%10s'%('%-.10s'%str(line_count_0_end)) + "\t" + str(float(line_count_0_end)/line_count)
			print ""

if __name__ == '__main__':
	if(len(sys.argv)<4):
		print "Usage:"
		print "	 python evaluate.py no_thresh/[thresh_file] no_gt/[groudtruth_file] [classify_result_file ...]"
		print "Note:"
		print "  1.阈值文件(第1列是label_index,第2列是阈值)可有可无。没有阈值的类，默认为阈值0.0；阈值为1.0的类，相当于把这个类过滤掉了。"
		print "  2.有groundtruth文件，就计算pr指标；否则，计算复审率指标。"
		exit()
	thresh_file = sys.argv[1]
	groudtruth_file = sys.argv[2]
	classify_result_file_list = []
	for i in range(3,len(sys.argv)):
			classify_result_file_list.append(sys.argv[i])
	evaluate = Evaluate()
	evaluate.read_thresh_file(thresh_file)
	evaluate.read_groudtruth_file(groudtruth_file)
	evaluate.process(classify_result_file_list)