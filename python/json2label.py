# coding=utf-8
# by hezhichao
# 2016.12.27

"""
__Author__: mashuai

__file description__: This file saves json operation functions.

"""
import sys
import json
import numpy as np

label_path = '/home/mashuai/work/name_label_table.txt'
class_num = 24

# read label-name from name_label_table
def read_label():
    name_dict = {}
    with open(label_path, 'r') as f:
        for line in f:
            line_list = line.split('\t')
            #print len(line_list)
            for i in range(1, len(line_list)):
                name = line_list[i].strip('\n')
                name = name.strip('\r')
                name_dict[ name ] = int(line_list[0])

    print name_dict
    return name_dict,len(name_dict)

def read_json(json_file_path):
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)
    return json_data

def gen_csv(json_file_path,img_path, data_path):
    json_data = read_json(json_file_path)
    name_dict,class_num = read_label()

    samp_num_arr = np.zeros((class_num),dtype=np.int32)
    print len(json_data)
    with open(data_path, 'ab') as f:
        for i in range(0, len(json_data)):
            if json_data[i]['label'] is not None:
                label = name_dict.get(json_data[i]['label'].strip(' '),-1)
                line = img_path+ json_data[i]['path'] + ' ' + str(label) +'\n'

                if label==-1:
                    print '%s %s' %(json_data[i]['label'].strip(' '), json_data[i]['path'])
                else:
                    samp_num_arr[label] += 1
                    f.write(line)
    print samp_num_arr
    #print sum(samp_num_arr)
    return samp_num_arr

if __name__ == '__main__':
    if(len(sys.argv)<5):
      print "python json2label.py label_path img_path output_path [json_file_path ...]"
      print "# example of label_path : ../rule/scene_label_name.csv"
      exit()
    label_path = sys.argv[1]
    img_path  = sys.argv[2]
    output_path = sys.argv[3]
    for i in range(4, len(sys.argv)):
        json_file_path  = sys.argv[i]
        print "No."+str(i-3)+":"+json_file_path
        gen_csv(json_file_path,img_path, output_path)
