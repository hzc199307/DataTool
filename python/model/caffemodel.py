# coding=utf-8
# by hezhichao
# 2017.03.25
# 对caffemodel的一些操作

import os
import json
import sys

sys.path.insert(0, '/home/hezhichao/work/gitprojects/caffe/python')
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()

class CaffeModel:

	def read(self,prototxt_file,caffemodel_file):
		self.net = caffe.Net(prototxt_file,caffemodel_file,caffe.TEST)

	def output_min_max(self,layer_list=None):
		min_value = 0.0
		max_value = 0.0
		params_count = 0
		params_low_count = 0
		for k,v in self.net.params.items():
			print k,v[0].data.shape
			params_count += len(v[0].data.flat)
			for value in v[0].data.flat:
				if value<0.01 and value>-0.01:
					params_low_count+=1
			min_value_ = min(v[0].data.flat)
			if min_value_<min_value:
				min_value = min_value_
			max_value_ = max(v[0].data.flat)
			if max_value_>max_value:
				max_value = max_value_
		print min_value,max_value
		print params_count,params_low_count

	def output_shape(self):
		for k,v in self.net.params.items():
			print k,v[0].data.shape

	def output_data(self):
		for k,v in self.net.params.items():
			print k,v[0].data,v[1].data

	def output_data_num(self):
		for k,v in self.net.params.items():
			print k,len(v[0].data.flat),len(v[1].data.flat)

	def change(self):
		print self.net.params["loss3/classifier_food101"][0].data
		self.net.params["loss3/classifier_food101"][0].data.flat[0]=11
		print self.net.params["loss3/classifier_food101"][0].data

	def set0(self,layer_list=None,lower_bound=-0.01,upper_bound=0.01):
		min_value = 0.0
		max_value = 0.0
		params_count = 0
		params_low_count = 0
		for k,v in self.net.params.items():
			FIND = False
			if layer_list!=None:
				for layer_name in layer_list:
					if k.find(layer_name)!=-1:
						FIND = True
						break
			if FIND==False:
				continue
			print k,v[0].data.shape,v[1].data.shape
			for i in range(0,2):
				params_count += len(v[i].data.flat)
				index = 0
				for value in v[i].data.flat:
					if value<0.01 and value>-0.01:
						params_low_count+=1
						v[i].data.flat[index]=0.0
					index+=1
				min_value_ = min(v[0].data.flat)
				if min_value_<min_value:
					min_value = min_value_
				max_value_ = max(v[0].data.flat)
				if max_value_>max_value:
					max_value = max_value_
		print min_value,max_value
		print params_count,params_low_count

	def save(self,save_path):
		self.net.save(save_path)
		print "caffemodel have been saved as "+save_path

if __name__ == '__main__':
	if (len(sys.argv) < 3):
		print "python caffemodel.py read prototxt_file caffemodel_file"
		print "python caffemodel.py set0 prototxt_file caffemodel_file save_caffemodel_path"
		exit()
	cmd = sys.argv[1]
	prototxt_file = sys.argv[2]
	caffemodel_file = sys.argv[3]
	caffeModel = CaffeModel()
	caffeModel.read(prototxt_file,caffemodel_file)
	if cmd=="read":
		caffeModel.output_min_max()
	elif cmd=="set0":
		save_caffemodel_path = sys.argv[4]
		caffeModel.set0(["4d","4e","5a","5b"])
		# v1 -0.01~0.01 params_count,params_low_count : 3961264 1507256 ; traindata7575 3961264 1494828; scene_v2_4_1_34k 3961264 1557181
		# v2 -0.1~0.1 params_count,params_low_count : 3961264 3935882
		# v3 -0.02~0.02 params_count,params_low_count : 3961264 2602494
		# v4 -0.005~0.005 params_count,params_low_count : 3961264 787543



		caffeModel.save(save_caffemodel_path)

	# caffeModel.output_data_num()
	# caffeModel.change()