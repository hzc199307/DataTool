# coding=utf-8
# by hezhichao
# 2017.03.27
# update 2017.03.27
# 用新的标注更新之前的groudtruth

import sys
import os

class UpdateGt:

	@staticmethod
	def process(rule,input_gt_file,update_gt_file_list,output_gt_file):
		dict_data_gt = {}
		input_gt_file_read = open(input_gt_file)
		for line in input_gt_file_read:
			strs = line.strip().split()
			dict_data_gt[strs[0]] = strs[1]
		input_gt_file_read.close()
		for update_gt_file in  update_gt_file_list:
			update_gt_file_read = open(update_gt_file)
			for line in update_gt_file_read:
				strs = line.strip().split()
				if rule == "not0" and strs[1]=="0":
					continue
				if dict_data_gt.has_key(strs[0]):
					dict_data_gt[strs[0]] = strs[1]
			update_gt_file_read.close()
		output_gt_file_write = open(output_gt_file,"w+")
		for key,value in dict_data_gt.items():
			output_gt_file_write.write(key+" "+value+"\n")
		output_gt_file_write.close()

if __name__ == '__main__':
	if(len(sys.argv)<5):
		print "Usage : 用新的标注更新之前的groudtruth"
		print "	python update_gt.py not0/all <input_gt_file> [<update_gt_file> ...] <output_gt_file>"
		print "	Note: not0表示只把新标注里面的非0label用上；all表示最后输出的gt以新标注为准。"
		exit()
	rule = sys.argv[1]
	input_gt_file = sys.argv[2]
	update_gt_file_list = []
	output_gt_file = sys.argv[-1]
	for i in range(3,len(sys.argv)-1):
			update_gt_file_list.append(sys.argv[i])
	UpdateGt.process(rule,input_gt_file,update_gt_file_list,output_gt_file)