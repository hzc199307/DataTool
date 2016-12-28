"""
__description__: This file combine the augment image file.
__ahthor__: MA Shuai
__date__: 2016-12-21
"""

import numpy as np
import time

src_files = ['tmp_img1.txt',
            'tmp_img2.txt',
            'tmp_img2.txt',
            'tmp_img3.txt',
            'tmp_img4.txt',
            'tmp_img5.txt',
            'tmp_img6.txt',
            'tmp_img7.txt',
            'tmp_img8.txt',
            'tmp_img9.txt']
des_file_path = 'vt_v1_4_2_1216_multi_class_with_170w_augment_train_img.txt'

if __name__ == '__main__':
    localtime = time.asctime( time.localtime(time.time()) )
    print localtime
    #time.sleep(36000)
    print 'start....'
    for i in range(0, len(src_files)):
        data = np.loadtxt(src_files[i], dtype=np.str, delimiter=" ")
        print '%d length is :%d' %(i,data.shape[0])
        with open(des_file_path, 'ab') as f:
            for j in range(0, data.shape[0]):
                f.write(data[j][0]+ ' '+ data[j][1] + '\n')
    print 'process over....'
    localtime = time.asctime( time.localtime(time.time()) )
    print localtime

