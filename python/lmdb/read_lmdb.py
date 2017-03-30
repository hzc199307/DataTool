# coding=utf-8
# by hezhichao
# create 2017.03.21
# update 2017.03.21
# 读取lmdb文件，并进行一些操作


import lmdb
import sys


sys.path.insert(0, '/home/hezhichao/work/caffe/python')
import caffe
caffe.set_device(0)
caffe.set_mode_gpu()

def count_data(lmdb_path):
	lmdb_env = lmdb.open(lmdb_path)
	lmdb_txn = lmdb_env.begin()
	lmdb_cursor = lmdb_txn.cursor()
	datum = caffe.proto.caffe_pb2.Datum()
	count = 0
	for key, value in lmdb_cursor:
		count+=1
		if count%10000==0:
			print count
		# datum.ParseFromString(value)
		# label = datum.label
		# data = caffe.io.datum_to_array(datum)
		# for l, d in zip(label, data):
		#		print l, d
	print "Count of LMDB:" + str(count)

if __name__ == '__main__':
	if(len(sys.argv)<2):
		print "python read_lmdb.py <lmdb_path>"
		exit()
	lmdb_path = sys.argv[1]
	count_data(lmdb_path)