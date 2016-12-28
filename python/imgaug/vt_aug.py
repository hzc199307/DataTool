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


# aug_arr =   np.array([0,5,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
# img_file_path = 'tmp_img1.txt'
# aug_arr = np.array([0,0,0,2,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
# img_file_path = 'tmp_img2.txt'
# aug_arr = np.array([0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
# img_file_path = 'tmp_img3.txt'
# aug_arr = np.array([0,0,0,0,0,0,0,0,3,5,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
# img_file_path = 'tmp_img4.txt'
# aug_arr = np.array([0,0,0,0,0,0,0,0,0,0,0,0,4,4,4,4,0,0,0,0,0,0,0,0,0,0])
# img_file_path = 'tmp_img5.txt'
# aug_arr = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,2,1,3,5,0,0,0,0,0])
# img_file_path = 'tmp_img6.txt'
# aug_arr = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,4,0,0])
# img_file_path = 'tmp_img7.txt'
# aug_arr = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0])
# img_file_path = 'tmp_img8.txt'
aug_arr = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
img_file_path = 'tmp_img9.txt'

## get program arguements
def get_args():
    ## argument
    #src_img_file_path = '/home/mashuai/work/greendam/data/vt_v1_4_2_1216_multi_class_with_110w_train_img.txt'
    #dest_img_path = '/home/mashuai/work/greendam/data/aug_data/vt_v1_4_2'
    parser = argparse.ArgumentParser(description='data augmentation ...')
    parser.add_argument('-s', '--src', type=str, required=True, help="src img file path")
    parser.add_argument('-d', '--destination', type=str, required=True, help="destination image path")

    args= parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    print args
    print 'start...'
    if os.path.exists(img_file_path):
        os.remove(img_file_path)
    data = np.loadtxt(args.src, dtype=np.str, delimiter=" ")
    for label in range(0, aug_arr.shape[0]):
        print 'start.....label %d......' %(label)
        if aug_arr[label] >0:
            count =0
            images= np.zeros((4000,256,256,3),dtype = np.uint8)
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
                    if count ==4000:
                        print 'label: %d, count: %d' %(label, count)
                        aug = Vt_augmenter(aug_arr[label])
                        aug.run_augment(images,args.destination, img_file_path, label)
                        count =0
                        images= np.zeros((4000,256,256,3),dtype = np.uint8)
            if count >0:
                print 'label: %d, count: %d' %(label, count)
                aug = Vt_augmenter(aug_arr[label])
                aug.run_augment(images[0:count,:,:,:], args.destination , img_file_path, label)
        print 'end.....label %d......' %(label)

