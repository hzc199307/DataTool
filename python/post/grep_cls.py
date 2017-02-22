# coding=utf-8
# by hezhichao
# 2017.02.13
# update 2017.02.13
# 挑出结果文件里面高于阈值的行

import sys
import os

class GrepCls:

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

	def process(self,classify_result_file_list,output_cls_file):
		output_cls_file_write = open(output_cls_file,"w+")
		for classify_result_file in classify_result_file_list:
			classify_result_file_read = open(classify_result_file)
			for line in classify_result_file_read:
				strs = line.strip().split()
				SAVE = False # 是否要在 output_cls_file 文件中写入这一行
				if len(strs)<4: # 没有分数
					if self.thresh_dict.has_key(int(strs[1])):
						SAVE = True
				else:
					BIGGER_THAN_THRESH = ( self.thresh_dict.has_key(int(strs[1])) and (float(strs[3+int(strs[1])].split(":")[1]) > self.thresh_dict[int(strs[1])]) )
					if BIGGER_THAN_THRESH:
						SAVE = True
				if SAVE:
					output_cls_file_write.write(line)
			classify_result_file_read.close()
		output_cls_file_write.close()

if __name__ == '__main__':
	if(len(sys.argv)<4):
		print "Usage:"
		print "	 python grep_cls.py [thresh_file] [classify_result_file ...] [output_cls_file]"
		print "Note:"
		print "  1.只会把thresh_file里面有的，且高于阈值的类别挑出来"
		print "  2.thresh_file第2列若没有阈值，默认阈值为0.0"
		print "  3.classify_result_file可以不是classify的结果文件，可以只是gt文件"
		exit()
	thresh_file = sys.argv[1]
	output_cls_file = sys.argv[len(sys.argv)-1]
	classify_result_file_list = []
	for i in range(2,len(sys.argv)-1):
			classify_result_file_list.append(sys.argv[i])
	grepCls = GrepCls()
	grepCls.read_thresh_file(thresh_file)
	grepCls.process(classify_result_file_list,output_cls_file)