"""
__description__: This file combine the augment image file.
__ahthor__: MA Shuai
__date__: 2016-12-21
"""

import numpy as np
import time
from vt_augmenter import read_json
import argparse

def get_args():
    ## argument
    parser = argparse.ArgumentParser(description='combine image temp files ...')
    parser.add_argument('-c', '--conf', type=str, required=True, help="json config file path")
    parser.add_argument('-s', '--sum', type=int, required=True, help="the sum of process")
    args= parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    print args
    config = read_json(args.conf)

    localtime = time.asctime( time.localtime(time.time()) )
    print localtime
    print 'start combine img....'
    for i in range(0, args.sum):
        tmp_file_path =os.path.join(config['output']['tmp_path'], "%d_tmp_file_path.txt" %(i)) 
        data = np.loadtxt(tmp_file_path, dtype=np.str, delimiter=" ")
        print '%d length is :%d' %(i,data.shape[0])
        with open(config['output']['path'], 'ab') as f:
            for j in range(0, data.shape[0]):
                f.write(data[j][0]+ ' '+ data[j][1] + '\n')
    print 'combine image file over....'



