"""

__author__: MA Shuai
__date__: 2016-12-17

"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ''))
import imgaug as ia
import augmenters as iaa
import numpy as np
from PIL import Image
from vt_augmenter import Vt_augmenter
import argparse
from vt_augmenter import read_json

## get program arguements
def get_args():
    ## argument

    parser = argparse.ArgumentParser(description='data augmentation ...')
    parser.add_argument('-c', '--conf', type=str, required=True, help="json config file path")
    parser.add_argument('-i', '--ith', type=int, required=True, help="the ith process")
    parser.add_argument('-s', '--sum', type=int, required=True, help="the sum of process")
    args= parser.parse_args()
    return args

def gen_aug_arr(ith,sum_process, class_num):
    ## ith start from 0
    if sum_process > class_num:
        print "ERROR: the process number must less than class number!!!"
        sys.exit(1)
    aug_arr = np.zeros((class_num))
    interval = class_num/sum_process
    split = class_num%sum_process
    if ith < split:
        for iter in range(0, interval+1):
            aug_arr[ith*(interval+1)+iter] = 1
    else:
        for iter in range(0, interval):
            aug_arr[split+ ith*interval+iter] = 1
    return aug_arr



if __name__ == '__main__':
    args = get_args()
    print args
    config = read_json(args.conf)
    print 'start...'
    class_num = len(config['label_config'])
    aug_arr = gen_aug_arr(args.ith,args.sum,class_num)
    print aug_arr
    tmp_file_path = config['output']['tmp_path'] + "%d_tmp_file_path.txt" %(args.ith)
    data = np.loadtxt(config['input']['path'], dtype=np.str, delimiter=" ")

    for label in range(0, aug_arr.shape[0]):
        print 'start.....label %d......' %(label)
        if aug_arr[label] >0:
            count =0
            images= np.zeros((2000,256,256,3),dtype = np.uint8)
            for i in range(0, data.shape[0]):
                if int(data[i][1]) == label:
                    try:
                        im = Image.open(data[i][0])
                        out = im.resize((256,256))
                        images[count] = np.asarray(out)
                        count +=1
                    except:
                        print 'error %s' %(data[i][0])
                        continue
                    if count ==2000:
                        print 'label: %d, count: %d' %(label, count)
                        aug = Vt_augmenter(config['label_config'][str(label)])
                        aug.run_augment(images,config['output']['img_path'], config['output']['tmp_path'], label)
                        count =0
                        images= np.zeros((2000,256,256,3),dtype = np.uint8)
            if count >0:
                print 'label: %d, count: %d' %(label, count)
                aug = Vt_augmenter( config['label_config'][str(label)] )
                aug.run_augment(images[0:count,:,:,:], config['output']['img_path'], config['output']['tmp_path'], label)
        print 'end.....label %d......' %(label)

