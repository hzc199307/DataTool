# coding=utf-8
# by hezhichao
# 2017.02.13
# update 2017.03.07
# 评价模型的Precision、Recall和ReviewRate

import sys
import os

from draw_tool import *

SCENE23_CLASS_LABELS = ['other', 'dance', 'gym', 'makeup', 'painting', 'calligraphy',
                'DJ','OtherInstrument',
                'Piano','Guitar','Violin','Saxophone','Guzheng','Erhu','Pipa','Harmonica','Harp',
                'Accordion','JazzDrum','Drum','Brass','Huangguanlei','WindInstrument']

class Tool:

	@staticmethod
	def get_lastname_of_path(path):
		return os.path.splitext(os.path.basename(path))[0]

	@staticmethod
	def get_groudtruth_dict(groudtruth_file):
		groudtruth_dict = {}
		if os.path.exists(groudtruth_file) == False:
			return
		groudtruth_file_read = open(groudtruth_file)
		for line in groudtruth_file_read:
			strs = line.strip().split()
			groudtruth_dict[str(strs[0])] = int(strs[1])
		groudtruth_file_read.close()
		return groudtruth_dict

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

	# 计算不同thresh下的Precision与Recall
	def process_tpr(self,classify_result_file_list,precision_thresh):
		# 必须要有真值表
		if len(self.groudtruth_dict)>0:
			tpr_tuple_list = []
			for classify_result_file in classify_result_file_list:
				tpr_tuple = PrecisionRecall.get_thresh_p_r(self.groudtruth_dict,classify_result_file)
				tpr_tuple_list.append(tpr_tuple)
			PrecisionRecall.print_thresh_p_r(tpr_tuple_list,precision_thresh)

	# 计算不同thresh下的Precision与Recall
	def draw_tprr(self,classify_result_file_list,precision_thresh):
		# 必须要有真值表
		if len(self.groudtruth_dict)>0:
			tpr_tuple_list = []
			for classify_result_file in classify_result_file_list:
				tpr_tuple = PrecisionRecall.get_thresh_p_r(self.groudtruth_dict,classify_result_file)
				tpr_tuple_list.append(tpr_tuple)
			PrecisionRecall.print_thresh_p_r(tpr_tuple_list,precision_thresh)

class ThreshPrecisionRecallReview:

	@staticmethod
	def draw(precision_groudtruth_file,precision_classify_result_file,recall_groudtruth_file,recall_classify_result_file,review_classify_result_file,output_dir):
		if output_dir[-1] != "/":
			output_dir += "/"
		curve_output_dir = output_dir + "tprr_curve/"
		if os.path.exists(curve_output_dir) == False:
			os.makedirs(curve_output_dir)
		table_output_dir = output_dir + "tprr_table/"
		if os.path.exists(table_output_dir) == False:
			os.makedirs(table_output_dir)
		max_index = -1
		dict_list = []
		total_legends = []
		print "calculating precision ..."
		if os.path.exists(precision_groudtruth_file) and os.path.exists(precision_classify_result_file):
			classify_result_file,max_cls_index,dict_cls__thresh_precision \
				= ThreshPrecisionRecallReview.get_thresh_precision( 
					Tool.get_groudtruth_dict(precision_groudtruth_file),
					precision_classify_result_file )
			dict_list.append(dict_cls__thresh_precision)
			total_legends.append("precision")
			if max_cls_index > max_index:
				max_index = max_cls_index
		print "calculating recall ..."
		if os.path.exists(recall_groudtruth_file) and os.path.exists(recall_classify_result_file):
			classify_result_file,max_cls_index,dict_cls__thresh_recall \
				= ThreshPrecisionRecallReview.get_thresh_recall( 
					Tool.get_groudtruth_dict(recall_groudtruth_file),
					recall_classify_result_file )
			dict_list.append(dict_cls__thresh_recall)
			total_legends.append("recall")
			if max_cls_index > max_index:
				max_index = max_cls_index
		print "calculating review ..."
		if os.path.exists(review_classify_result_file):
			classify_result_file,max_cls_index,dict_cls__thresh_review \
				= ThreshPrecisionRecallReview.get_thresh_review( review_classify_result_file )
			dict_list.append(dict_cls__thresh_review)
			total_legends.append("review")
			if max_cls_index > max_index:
				max_index = max_cls_index
		print "writing table ..."
		for j in range(0,len(dict_list)):
			sub_table_output_dir = table_output_dir+"thresh_"+total_legends[j]+"/"
			if os.path.exists(sub_table_output_dir) == False:
				os.makedirs(sub_table_output_dir)
			for i in range(1,max_index+1):
				if dict_list[j].has_key(i):
					name = str(i)+"_"+SCENE23_CLASS_LABELS[i]+"_thresh_"+total_legends[j]
					file_output = open(sub_table_output_dir + name + ".csv","w+")
					file_output.write("thresh\t"+total_legends[j] + "\n")
					xs,ys = dict_list[j][i]
					for k in range(0,len(xs)):
						if xs[k]<0.8: # 只保留大于0.8的部分 TODO
							continue
						file_output.write(str(xs[k]) + "\t" + str(ys[k]) + "\n")
					file_output.close()
		print "drawing curve ..."
		for i in range(1,max_index+1): # 跳过了0
			data_list = []
			legends = []
			for j in range(0,len(dict_list)):
				if dict_list[j].has_key(i):
					data_list.append(dict_list[j][i])
					legends.append(total_legends[j])
			if len(legends)>0:
				name = str(i)+"_"+SCENE23_CLASS_LABELS[i]
				DrawTool.draw_for_tprr(data_list,legends,name,curve_output_dir+name+".png")

	@staticmethod
	def write(precision_groudtruth_file,precision_classify_result_file,recall_groudtruth_file,recall_classify_result_file,review_classify_result_file,output_dir):
		if output_dir[-1] != "/":
			output_dir += "/"
		output_dir += "tprr_table/"
		if os.path.exists(output_dir) == False:  
			os.makedirs(output_dir)
		max_index = -1
		dict_list = []
		total_legends = []
		print "calculating precision ..."
		if os.path.exists(precision_groudtruth_file) and os.path.exists(precision_classify_result_file):
			classify_result_file,max_cls_index,dict_cls__thresh_precision \
				= ThreshPrecisionRecallReview.get_thresh_precision( 
					Tool.get_groudtruth_dict(precision_groudtruth_file),
					precision_classify_result_file )
			dict_list.append(dict_cls__thresh_precision)
			total_legends.append("precision")
			if max_cls_index > max_index:
				max_index = max_cls_index
		print "calculating recall ..."
		if os.path.exists(recall_groudtruth_file) and os.path.exists(recall_classify_result_file):
			classify_result_file,max_cls_index,dict_cls__thresh_recall \
				= ThreshPrecisionRecallReview.get_thresh_recall( 
					Tool.get_groudtruth_dict(recall_groudtruth_file),
					recall_classify_result_file )
			dict_list.append(dict_cls__thresh_recall)
			total_legends.append("recall")
			if max_cls_index > max_index:
				max_index = max_cls_index
		print "calculating review ..."
		if os.path.exists(review_classify_result_file):
			classify_result_file,max_cls_index,dict_cls__thresh_review \
				= ThreshPrecisionRecallReview.get_thresh_review( review_classify_result_file )
			dict_list.append(dict_cls__thresh_review)
			total_legends.append("review")
			if max_cls_index > max_index:
				max_index = max_cls_index
		print "writing ..."
		for i in range(1,max_index+1): # 跳过了0
			data_list = []
			legends = []
			for j in range(0,len(dict_list)):
				if dict_list[j].has_key(i):
					data_list.append(dict_list[j][i])
					legends.append(total_legends[j])
			if len(legends)>0:
				name = str(i)+"_"+SCENE23_CLASS_LABELS[i]
				DrawTool.draw_for_tprr(data_list,legends,name,output_dir+name+".png")

	@staticmethod
	def __preprocess(groudtruth_dict,classify_result_file):
		dict_gt_count = {}
		classify_result_file_read = open(classify_result_file)
		max_cls_index = -1
		dict_cls_scores={}
		for line in classify_result_file_read:
			strs = line.strip().split()
			if groudtruth_dict != None:
				if groudtruth_dict.has_key(strs[0]) == False: # TODO 可能将来要删除
					continue
				gt = groudtruth_dict[strs[0]]
				if gt > max_cls_index:
					max_cls_index = gt
				if int(strs[1]) > max_cls_index:
					max_cls_index = int(strs[1])
				if dict_gt_count.has_key(gt):
					dict_gt_count[gt] += 1
				else:
					dict_gt_count[gt] = 1
				# 这是记录分数
				for i in range(3,len(strs)):
					cls,score = strs[i].split(":")
					if dict_cls_scores.has_key(int(cls)):
						dict_cls_scores[int(cls)].append( (float(score),int(cls)==gt) )
					else:
						dict_cls_scores[int(cls)] = []
			else:
				# 这是记录分数
				for i in range(3,len(strs)):
					cls,score = strs[i].split(":")
					if dict_cls_scores.has_key(int(cls)):
						dict_cls_scores[int(cls)].append( float(score) )
					else:
						dict_cls_scores[int(cls)] = []
		classify_result_file_read.close()
		return (dict_gt_count,max_cls_index,dict_cls_scores)

	@staticmethod
	def get_thresh_p_r(groudtruth_dict,classify_result_file):
		(dict_gt_count,max_cls_index,dict_cls_scores) = ThreshPrecisionRecallReview.__preprocess(groudtruth_dict,classify_result_file)
		dict_cls__thresh_p_r = {}
		for cls,scores in dict_cls_scores.items():
			scores.sort()
			predict_count = len(scores) # precision的分母（它会随着阈值的升高，不断减少）
			if dict_gt_count.has_key(cls):
				gt_count = dict_gt_count[cls] # recall的分母（它不会变）
				correct_count = dict_gt_count[cls] # precision和recall的分子（它会随着阈值的升高，不断减少）
			else:
				continue # 如果真实情况没有此类别，则无法计算precision和recall
			dict_cls__thresh_p_r[cls] = []
			next_index = 0
			len_scores = len(scores)
			for (score,correct) in scores:
				next_index += 1
				thresh = score 
				if correct == True:
					correct_count -= 1
				predict_count -= 1
				# 如果 没有走到尽头 或者 下个分数不一样，才把tpr加进去
				if next_index != len_scores and scores[next_index][0]!=score:
					precision = float(correct_count)/predict_count
					recall = float(correct_count)/gt_count
					dict_cls__thresh_p_r[cls].append((thresh,precision,recall))
		return (classify_result_file,dict_cls__thresh_p_r)

	@staticmethod
	def get_thresh_precision(groudtruth_dict,classify_result_file):
		(dict_gt_count,max_cls_index,dict_cls_scores) = ThreshPrecisionRecallReview.__preprocess(groudtruth_dict,classify_result_file)
		dict_cls__thresh_precision = {}
		for cls,scores in dict_cls_scores.items():
			scores.sort()
			predict_count = len(scores) # precision的分母（它会随着阈值的升高，不断减少）
			if dict_gt_count.has_key(cls):
				correct_count = dict_gt_count[cls] # precision和recall的分子（它会随着阈值的升高，不断减少）
			else:
				continue # 如果真实情况没有此类别，则无法计算precision和recall
			dict_cls__thresh_precision[cls] = ([],[])
			next_index = 0
			len_scores = len(scores)
			for (score,correct) in scores:
				next_index += 1
				thresh = score 
				predict_count -= 1
				if correct == True:
					correct_count -= 1
				# 一般阈值只会取0.5以上的值
				# if thresh<0.5:
				# 		continue
				# 如果 没有走到尽头 或者 下个分数不一样，才把tpr加进去
				if next_index != len_scores and scores[next_index][0]!=score:
					precision = float(correct_count)/predict_count
					dict_cls__thresh_precision[cls][0].append(thresh)
					dict_cls__thresh_precision[cls][1].append(precision)
		return (classify_result_file,max_cls_index,dict_cls__thresh_precision)

	@staticmethod
	def get_thresh_recall(groudtruth_dict,classify_result_file):
		(dict_gt_count,max_cls_index,dict_cls_scores) = ThreshPrecisionRecallReview.__preprocess(groudtruth_dict,classify_result_file)
		dict_cls__thresh_recall = {}
		for cls,scores in dict_cls_scores.items():
			scores.sort()
			predict_count = len(scores) # precision的分母（它会随着阈值的升高，不断减少）
			if dict_gt_count.has_key(cls):
				gt_count = dict_gt_count[cls] # recall的分母（它不会变）
				correct_count = dict_gt_count[cls] # precision和recall的分子（它会随着阈值的升高，不断减少）
			else:
				continue # 如果真实情况没有此类别，则无法计算precision和recall
			dict_cls__thresh_recall[cls] = ([],[])
			next_index = 0
			len_scores = len(scores)
			for (score,correct) in scores:
				next_index += 1
				thresh = score 
				if correct == True:
					correct_count -= 1
				# 一般阈值只会取0.5以上的值
				# if thresh<0.5:
				# 		continue
				# 如果 没有走到尽头 或者 下个分数不一样，才把tpr加进去
				if next_index != len_scores and scores[next_index][0]!=score:
					recall = float(correct_count)/gt_count
					dict_cls__thresh_recall[cls][0].append(thresh)
					dict_cls__thresh_recall[cls][1].append(recall)
		return (classify_result_file,max_cls_index,dict_cls__thresh_recall)

	@staticmethod
	def get_thresh_review(classify_result_file):
		(dict_gt_count,max_cls_index,dict_cls_scores) = ThreshPrecisionRecallReview.__preprocess(None,classify_result_file)
		dict_cls__thresh_review = {}
		for cls,scores in dict_cls_scores.items():
			scores.sort()
			total_count = len(scores) # precision的分母（它会随着阈值的升高，不断减少）
			review_count = total_count
			dict_cls__thresh_review[cls] = ([],[])
			next_index = 0
			len_scores = len(scores)
			for score in scores:
				next_index += 1
				thresh = score 
				review_count -= 1
				if thresh < 0.34:
					continue
				# 如果 没有走到尽头 或者 下个分数不一样，才把tpr加进去
				if next_index != len_scores and scores[next_index]!=score:
					review = float(review_count)/total_count
					dict_cls__thresh_review[cls][0].append(thresh)
					dict_cls__thresh_review[cls][1].append(review)
		return (classify_result_file,max_cls_index,dict_cls__thresh_review)

class PrecisionRecall:

	# 计算PR，并且返回
	@staticmethod
	def calculate_precision_recall(thresh_dict,groudtruth_dict,classify_result_file,NEED_dict_cls_scores = False):
		dict_correct = {}
		dict_predict_count = {}
		dict_gt_count = {}
		classify_result_file_read = open(classify_result_file)
		max_cls_index = 0
		dict_cls_scores={}
		for line in classify_result_file_read:
			strs = line.strip().split()
			NO_THRESH = ( thresh_dict.has_key(int(strs[1])) == False )
			BIGGER_THAN_THRESH = ( thresh_dict.has_key(int(strs[1])) and (float(strs[3+int(strs[1])].split(":")[1]) > thresh_dict[int(strs[1])]) )
			cls = int(strs[1])
			if (NO_THRESH or BIGGER_THAN_THRESH) == False:
				cls = 0
			if groudtruth_dict.has_key(strs[0]) == False: # TODO 可能将来要删除
				continue
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
			# 这是记录分数
			if NEED_dict_cls_scores == True:
				for i in range(3,len(strs)):
					cls,score = strs[i].split(":")
					if dict_cls_scores.has_key(int(cls)):
						dict_cls_scores[int(cls)].append( (float(score),int(cls)==gt) )
					else:
						dict_cls_scores[int(cls)] = []
		classify_result_file_read.close()
		if NEED_dict_cls_scores == True:
			return (dict_gt_count,max_cls_index,dict_cls_scores)
		else:
			return (classify_result_file,dict_correct,dict_predict_count,dict_gt_count,max_cls_index)

	@staticmethod
	def get_thresh_p_r(groudtruth_dict,classify_result_file):
		(dict_gt_count,max_cls_index,dict_cls_scores) = PrecisionRecall.calculate_precision_recall({},groudtruth_dict,classify_result_file,True)
		dict_cls__thresh_p_r = {}
		for cls,scores in dict_cls_scores.items():
			scores.sort()
			predict_count = len(scores) # precision的分母（它会随着阈值的升高，不断减少）
			if dict_gt_count.has_key(cls):
				gt_count = dict_gt_count[cls] # recall的分母（它不会变）
				correct_count = dict_gt_count[cls] # precision和recall的分子（它会随着阈值的升高，不断减少）
			else:
				continue # 如果真实情况没有此类别，则无法计算precision和recall
			dict_cls__thresh_p_r[cls] = []
			next_index = 0
			len_scores = len(scores)
			for (score,correct) in scores:
				next_index += 1
				thresh = score 
				if correct == True:
					correct_count -= 1
				predict_count -= 1
				# 如果 没有走到尽头 或者 下个分数不一样，才把tpr加进去
				if next_index != len_scores and scores[next_index][0]!=score:
					precision = float(correct_count)/predict_count
					recall = float(correct_count)/gt_count
					dict_cls__thresh_p_r[cls].append((thresh,precision,recall))
		return (classify_result_file,dict_cls__thresh_p_r)

	@staticmethod
	def print_thresh_p_r(tpr_tuple_list,precision_thresh):
		for (classify_result_file,dict_cls__thresh_p_r) in tpr_tuple_list:
			print "TPR " + classify_result_file
			print "index\tprecision\trecall\tthresh"
			for cls,thresh_p_r_list in dict_cls__thresh_p_r.items():
				tmp = 0
				length = len(thresh_p_r_list)
				for (thresh,precision,recall) in thresh_p_r_list:
					tmp += 1
					# if thresh > 0.5:
					# 	print thresh,precision,recall
					if precision>=precision_thresh or tmp>=length:
						print str(cls) + "\t" + '%-10s'%('%-.5s'%str(precision)) + "\t" + '%-.5s'%str(recall) + "\t" + str(thresh) 
						break
			print ""

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
				print str(cls) + "\t" + '%-10s'%('%-.5s'%str(precision)) + "\t" + '%-.5s'%str(recall) + "\t" + '%7s'%str(fenzi) + "\t" + '%13s'%str(precision_fenmu) + "\t" + '%8s'%str(recall_fenmu)
				fenzi_sum += fenzi
				fenmu_sum += precision_fenmu
				if cls != 0:
					fenzi_sum_1_end += fenzi
					precision_fenmu_sum_1_end += precision_fenmu
					recall_fenmu_sum_1_end += recall_fenmu
			print "all\t" + '%-10s'%('%-.5s'%str(float(fenzi_sum)/fenmu_sum)) + "\t" + '%-.5s'%str(float(fenzi_sum)/fenmu_sum) + "\t" + '%7s'%str(fenzi_sum) + "\t" + '%13s'%str(fenmu_sum) + "\t" + '%8s'%str(fenmu_sum)
			print "1-end\t" + '%-10s'%('%-.5s'%str(float(fenzi_sum_1_end)/precision_fenmu_sum_1_end)) + "\t" + '%-.5s'%str(float(fenzi_sum_1_end)/recall_fenmu_sum_1_end) + "\t" + '%7s'%str(fenzi_sum_1_end) + "\t" + '%13s'%str(precision_fenmu_sum_1_end) + "\t" + '%8s'%str(recall_fenmu_sum_1_end)
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
					review_num = 0
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
		print "Usage 3: 计算不同thresh下的Precision与Recall"
		print "	python evaluate.py tpr <groudtruth_file> $precision [<classify_result_file> ...]"
		print "Usage 4:"
		print "	python evaluate.py draw_tprr <precision_groudtruth_file> <precision_classify_result_file> "
		print "								 <recall_groudtruth_file> <recall_classify_result_file>"
		print "								 <review_classify_result_file> <output_dir>"
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
	elif sys.argv[1] == "tpr" or sys.argv[1] == "TPR":
		groudtruth_file = sys.argv[2]
		precision_thresh = float(sys.argv[3])
		classify_result_file_list = []
		for i in range(4,len(sys.argv)):
				classify_result_file_list.append(sys.argv[i])
		evaluate = Evaluate()
		evaluate.read_groudtruth_file(groudtruth_file)
		evaluate.process_tpr(classify_result_file_list,precision_thresh)
	elif sys.argv[1] == "draw_tprr" or sys.argv[1] == "DRAW_TPRR":
		ThreshPrecisionRecallReview.draw( 
			sys.argv[2], sys.argv[3],
			sys.argv[4], sys.argv[5],
			sys.argv[6], sys.argv[7], )