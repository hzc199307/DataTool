# coding=utf-8
# by hezhichao
# create 2017.02.04
# update 2017.02.04
# 根据一个label_gt对照表，把label变成用于训练的groundtruth

import os
import sys
import json

class Label2gt:

	def __init__(self,rule_json_file):
		self.rule_jsons = json.load(open(rule_json_file))

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
				file_read.close()
			file_output.close()

if __name__ == '__main__':
    if(len(sys.argv)<2):
      print "python label2gt.py rule_json_file"
      exit()
    rule_json_file = sys.argv[1]
    label2gt = Label2gt(rule_json_file)
    label2gt.process()