# coding=utf-8
# by hezhichao
# 2017.03.07
# update 2017.03.07
# 根据数据的lst文件，以及映射规则，给数据自动加上groudtruth

import sys
import os

class Lst2Gt:

	@staticmethod
	def process(rule_file,input_lst_file_list,output_gt_file):
		# 读取规则文件
		rule_list = []
		if os.path.exists(rule_file) == False:
			print "规则文件不存在"
			return
		rule_file_read = open(rule_file)
		count = 0
		for line in rule_file_read:
			strs = line.strip().split()
			if len(strs)>1:
				rule_list.append( (strs[0],int(strs[1])) ) #以元组的方式储存规则
			else:
				rule_list.append( (strs[0],count) ) #以元组的方式储存规则
			count += 1
		rule_file_read.close()
		# 读取输入文件，匹配规则，并且将gt记录在输出文件
		output_gt_file_write = open(output_gt_file,"w+")
		for input_lst_file in input_lst_file_list:
			input_lst_file_read = open(input_lst_file)
			for line in input_lst_file_read:
				gt = "-"
				for (match_str,cls) in rule_list:
					if line.find(match_str)!= -1:
						gt = cls
						break
				output_gt_file_write.write(line.strip()+" "+str(gt)+"\n")
			input_lst_file_read.close()
		output_gt_file_write.close()

if __name__ == '__main__':
	if(len(sys.argv)<4):
		print "Usage : 给lst自动加上groudtruth"
		print "	python lst2gt.py <rule_file> [<input_lst_file> ...] <output_gt_file>"
		print "	Note: 如果数据没有对应类别，则给一个'-'"
		exit()
	rule_file = sys.argv[1]
	input_lst_file_list = []
	output_gt_file = sys.argv[-1]
	for i in range(2,len(sys.argv)-1):
			input_lst_file_list.append(sys.argv[i])
	Lst2Gt.process(rule_file,input_lst_file_list,output_gt_file)
