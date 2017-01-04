# coding=utf-8
# by hezhichao
# 2016.12.10
# update 2017.01.04

import sys
import json

import md5
import os

class Md5Tool:

    @staticmethod
    def sumfile(fobj):    
        m = md5.new()
        while True:
            d = fobj.read(8096)
            if not d:
                break
            m.update(d)
        return m.hexdigest()

    @staticmethod
    def md5sum(fname):    
        if fname == '-':
            ret = sumfile(sys.stdin)
        else:
            try:
                f = file(fname, 'rb')
            except:
                return 'Failed to open file'
            ret = Md5Tool.sumfile(f)
            f.close()
        return ret

class DataProcess:

    def read_dp_json(self,dp_json_file):
        self.dp_json = json.load(open(dp_json_file))

    def process(self):
        for dp_json in self.dp_json:
            if dp_json.has_key("name"):
                print "#----------- "+str(dp_json["name"])
            else:
                print "#-----------"
            if dp_json.has_key("skip") and str(dp_json["skip"])=="True":
                print "skip...\n"
                continue
            type = dp_json["process"]["type"];
            if type == "merge":
                self.dp_by_merge(dp_json)
            elif type == "md5":
                self.dp_by_md5(dp_json)
            elif type == "times":
                self.dp_by_times(dp_json)
            elif type == "target":
                self.dp_by_target(dp_json)
            elif type == "split":
                self.dp_by_split(dp_json)
            print ""

    def dp_by_merge(self, dp_json):
        file_out = open(dp_json["output"]["path"], "w+")
        for file_in_path in dp_json["input"]["path"]:
            file_in = open(file_in_path)
            for line in file_in:
                file_out.write(line)
            file_in.close()
        file_out.close()

    def dp_by_md5(self,dp_json):
        file_out = open(dp_json["output"]["path"],"w+")
        count = 0
        for file_in_path in  dp_json["input"]["path"]:
            file_in = open(file_in_path)
            for line in file_in:
                strs = line.strip().split()
                file_out.write(Md5Tool.md5sum(strs[0])+" "+strs[1]+"\n")
                count += 1
                if ( count%100 == 0):
                    print "Processed "+str(count)+" files."
            file_in.close()
        file_out.close()

    def dp_by_times(self,dp_json):
        label_num = dp_json["process"]["label_num"]
        file_out = open(dp_json["output"]["path"],"w+")
        for file_in_path in  dp_json["input"]["path"]:
            file_in = open(file_in_path)
            for line in file_in:
                strs = line.strip().split()
                times = label_num[strs[1]]
                while (times>0):
                    file_out.write(line)
                    times = times - 1
            file_in.close()
        file_out.close()

    def dp_by_target(self,dp_json):
        label_num = dp_json["process"]["label_num"]
        file_out = open(dp_json["output"]["path"]+"_", "w+")
        output_type = "gt"
        if dp_json["output"].has_key("type"):
            output_type = dp_json["output"]["type"]
        label_count = {}
        for file_in_path in dp_json["input"]["path"]:
            file_in = open(file_in_path)
            for line in file_in:
                strs = line.strip().split()
                if label_count.has_key(strs[1]):
                    label_count[strs[1]] += 1
                else:
                    label_count[strs[1]] = 1
            file_in.close()
        times = {}
        index_end = {}
        for label,count in label_count.items():
            if label_num[label] == -1:
                times[label] = 1
                index_end[label] = count
            else:
                times[label] = (label_num[label]-1)/count + 1
                index_end[label] = (label_num[label]-1)%count + 1
        for file_in_path in dp_json["input"]["path"]:
            file_in = open(file_in_path)
            for line in file_in:
                strs = line.strip().split()
                _times = times[strs[1]]
                if index_end[strs[1]] >0:
                    index_end[strs[1]] -= 1
                else:
                    _times -= 1
                while (_times > 0):
                    if output_type == "lst":
                        file_out.write(strs[0]+"\n")
                    else:
                        file_out.write(line)
                    _times = _times - 1
            file_in.close()
        file_out.close()
        os.system('cat '+str(dp_json["output"]["path"])+'_ | shuf > '+ str(dp_json["output"]["path"]))
        os.system('rm '+str(dp_json["output"]["path"])+'_')

    def dp_by_split(self,dp_json):
        label_num = dp_json["process"]["label_num"]
        file_out_train = open(dp_json["output"]["train_path"], "w+")
        file_out_test = open(dp_json["output"]["test_path"], "w+")
        label_count = {}
        for file_in_path in dp_json["input"]["path"]:
            file_in = open(file_in_path)
            for line in file_in:
                strs = line.strip().split()
                if label_count.has_key(strs[1]):
                    label_count[strs[1]] += 1
                else:
                    label_count[strs[1]] = 1
            file_in.close()
        times = {}
        index_end = {}
        for label, count in label_count.items():
            print "label="+str(label)
            if label_num.has_key(label) == False:
                label_num[label] = 0
            if label_num[label] == -1:
                times[label] = 1
                index_end[label] = count
            else:
                times[label] = (label_num[label] - 1) / count + 1
                index_end[label] = (label_num[label] - 1) % count + 1
        for file_in_path in dp_json["input"]["path"]:
            file_in = open(file_in_path)
            for line in file_in:
                strs = line.strip().split()
                _times = times[strs[1]]
                if index_end[strs[1]] > 0:
                    index_end[strs[1]] -= 1
                else:
                    _times -= 1
                if (_times > 0):
                    file_out_test.write(line)
                    _times = _times - 1
                else:
                    file_out_train.write(line)
            file_in.close()
        file_out_train.close()
        file_out_test.close()

if __name__ == '__main__':
    if(len(sys.argv)<2):
      print "python data_process.py dp_json_file"
      print "# example of dp_json_file : ../../rule/scene_v1_5.split.dp.json"
      exit()
    dp_json_file = sys.argv[1]
    dataProcess = DataProcess()
    dataProcess.read_dp_json(dp_json_file)
    dataProcess.process()
