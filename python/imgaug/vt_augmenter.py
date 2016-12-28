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
import hashlib
import parameters as iap
import time

def get_md5_value(src):

    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

class Vt_augmenter:

    def __init__(self,num):
        self.__aug_num = num

    def set_aug_num(self, num):
        self.__aug_num = num

    def __change_brightness(self, images):
        #applies the given augmenter in 50% of all cases,
        st = lambda aug: iaa.Sometimes(0.5, aug)
        print images.shape
        seq = iaa.Sequential([
            st(iaa.Add((-50, 50), per_channel=1)), # change brightness of images (by -40 to 40 of original value)
            st(iaa.Multiply((0.6, 1.4), per_channel=1)) # change brightness of images (50-150% of original value)
            ],  random_order=True)
        images_aug = seq.augment_images(images)
        return images_aug

    def __gaussian_blur(self, images):
        print images.shape
        # Blur by a value sigma which is sampled from a uniform distribution
        # of range 0.1 <= x < 2.5.
        # The convenience shortcut for this is: iaa.GaussianBlur((0.1, 2.5))
        blurer = iaa.GaussianBlur(iap.Uniform(0.1, 3.0))
        images_aug = blurer.augment_images(images)
        return images

    def __gaussian_noise(self, images):
        #applies the given augmenter in 50% of all cases,
        st = lambda aug: iaa.Sometimes(1, aug)
        print images.shape
        seq = iaa.Sequential([
            st(iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.15), per_channel=0.5)) # add gaussian noise to images
            ],  random_order=True)
        images_aug = seq.augment_images(images)
        return images_aug
        

    def __dropout(self, images):
        #applies the given augmenter in 50% of all cases,
        st = lambda aug: iaa.Sometimes(1, aug)
        print images.shape
        seq = iaa.Sequential([
            st(iaa.Dropout((0.0, 0.1), per_channel=1)) # randomly remove up to 10% of the pixels
            ],  random_order=True)
        images_aug = seq.augment_images(images)
        return images_aug

    def __contrast_norm(self, images):
        #applies the given augmenter in 50% of all cases,
        st = lambda aug: iaa.Sometimes(0.5, aug)
        print images.shape
        seq = iaa.Sequential([
            st(iaa.ContrastNormalization((0.4, 2.0), per_channel=1)), # improve or worsen the contrast
            st(iaa.ContrastNormalization((0.4, 2.0), per_channel=0.5)), # improve or worsen the contrast
            ],  random_order=True)
        images_aug = seq.augment_images(images)
        return images_aug

    def __affine(self, images):
        #applies the given augmenter in 50% of all cases,
        st = lambda aug: iaa.Sometimes(1, aug)

        seq = iaa.Sequential([
            st(iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)}, # scale images to 80-120% of their size, individually per axis
            translate_px={"x": (-16, 16), "y": (-16, 16)}, # translate by -16 to +16 pixels (per axis)
            rotate=(-30, 30), # rotate by -30 to +30 degrees
            shear=(-16, 16), # shear by -16 to +16 degrees
            order=ia.ALL, # use any of scikit-image's interpolation methods
            cval=(0, 1.0), # if mode is constant, use a cval between 0 and 1.0
            mode='constant' # use any of scikit-image's warping modes (see 2nd image from the top for examples)
            ))
            ],  random_order=True)
        images_aug = seq.augment_images(images)
        return images_aug

    def __elastic_transformation(self, images):
        #applies the given augmenter in 50% of all cases,
        st = lambda aug: iaa.Sometimes(1, aug)
        print images.shape
        seq = iaa.Sequential([
            st(iaa.ElasticTransformation(alpha=(0.5, 3.5), sigma=0.25)) # apply elastic transformations with random strengths
            ],  random_order=True)
        images_aug = seq.augment_images(images)
        return images_aug
    
    def __mix_op(self, images):
        st = lambda aug: iaa.Sometimes(0.5, aug)

        # Define our sequence of augmentation steps that will be applied to every image
        # All augmenters with per_channel=0.5 will sample one value _per image_
        # in 50% of all cases. In all other cases they will sample new values
        # _per channel_.
        seq = iaa.Sequential([
                st(iaa.Crop(percent=(0, 0.1))), # crop images by 0-10% of their height/width
                st(iaa.GaussianBlur((0, 3.0))), # blur images with a sigma between 0 and 3.0
                st(iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.2), per_channel=0.5)), # add gaussian noise to images
                st(iaa.Add((-50, 50), per_channel=0.5)), # change brightness of images (by -10 to 10 of original value)
                st(iaa.Multiply((0.5, 1.5), per_channel=0.5)), # change brightness of images (50-150% of original value)
                st(iaa.ContrastNormalization((0.5, 2.0), per_channel=0.5)) # improve or worsen the contrast
            ],
            random_order=True # do all of the above in random order
        )
        print images.shape
        images_aug = seq.augment_images(images)
        print images_aug.shape
        return images_aug

    def __save_images(self, images_aug, dest_img_path, img_file, label):
        l = []
        print images_aug.shape
        for i in range(0, images_aug.shape[0]):
            im = Image.fromarray(images_aug[i])
            name = os.path.join(dest_img_path, get_md5_value(images_aug[i,:,:,0].tostring())+'.jpg')
            im.save(name)
            l.append(name)
        with open (img_file,'ab') as f:
            for i in range(0, len(l)):
                f.write(l[i] +' '+ str(label)+'\n')

    #augment the data max augmentation number is 13
    def run_augment(self, images,dest_img_path, img_file, label):
        count=0
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__change_brightness(images)
            print '__change_brightness over!!!!!!!!!!!!'
            #self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__affine(images)
            print '__affine over!!!!!!!!!!!!'
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__mix_op(images)
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            print '__mix_op over!!!!!!!!!!!!'
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__contrast_norm(images)
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            print '__contrast_norm over!!!!!!!!!!'
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__change_brightness(images)
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            print '__contrast_norm over!!!!!!!!!!'
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__dropout(images)
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            print '__dropout over!!!!!!!!!!'
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__gaussian_blur(images)
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            print '__gaussian_blur over!!!!!!!!!!'
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__change_brightness(images)
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            print '__change_brightness over!!!!!!!!!!'
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__contrast_norm(images)
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            print '__contrast_norm over!!!!!!!!!!'
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__mix_op(images)
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            print '__mix_op over!!!!!!!!!!'
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__elastic_transformation(images)
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            print '__elastic_transformation over!!!!!!!!!!'
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__change_brightness(images)
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            print '__change_brightness over!!!!!!!!!!'
        count +=1
        if count < self.__aug_num:
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            images_aug = self.__mix_op(images)
            self.__save_images(images_aug, dest_img_path, img_file, label)
            localtime = time.asctime( time.localtime(time.time()) )
            print localtime
            print '__mix_op over!!!!!!!!!!'









        


    

