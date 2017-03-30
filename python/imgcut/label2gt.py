# coding=utf-8
# by hezhichao
# create 2017.02.04
# update 2017.02.04
# 根据一个label_gt对照表，把label变成用于训练的groundtruth

import os
import sys
import json

#递归的把list和dict里的Unicode对象encode成str,解决json读取中文乱码的问题
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class Label2gt:

	def __init__(self,rule_json_file):
		self.rule_jsons = json.load(open(rule_json_file))
		self.rule_jsons = byteify(self.rule_jsons)

	def process(self):
		for rule_json in self.rule_jsons:
			if rule_json.has_key("name"):
				print rule_json["name"]
			rule = rule_json["process"]["label_gt"]
			file_output = open(rule_json["output"]["gt"],"w+")
			for file_ in rule_json["input"]:
				file_read = open(file_["file"])
				prefix = file_["rootfolder"]
				for line in file_read:
					strs = line.strip().split()
					if rule.has_key(strs[1]): # 对照表里面没有的就跳过
						file_output.write(prefix + strs[0] + " " + str(rule[strs[1]]) + "\n")
					else:
						print strs[1]
				file_read.close()
			file_output.close()

if __name__ == '__main__':
    if(len(sys.argv)<2):
      print "python label2gt.py rule_json_file"
      exit()
    rule_json_file = sys.argv[1]
    label2gt = Label2gt(rule_json_file)
    label2gt.process()